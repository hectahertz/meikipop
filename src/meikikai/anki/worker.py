# meikikai/anki/worker.py
import logging
import queue
import threading
from dataclasses import dataclass
from html import escape
from pathlib import Path
from uuid import uuid4

from PyQt6.QtCore import QObject, pyqtSignal

from meikikai.anki.cards import build_vocab_card_payload
from meikikai.anki.connect import (
    AnkiApiError,
    AnkiConnectClient,
    AnkiConnectionError,
    AnkiModelSetupError,
    DuplicateNoteError,
    make_note,
    note_exists_for_key,
    setup_meikikai_note_type,
)
from meikikai.config.config import config

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AnkiExportRequest:
    lookup_data: object
    screenshot_path: str | None = None


class AnkiExportNotifier(QObject):
    message = pyqtSignal(str, str, str)


class AnkiExportWorker(threading.Thread):
    def __init__(self, anki_url: str, deck_name: str, model_name: str, notifier: AnkiExportNotifier):
        super().__init__(daemon=True, name="AnkiExportWorker")
        self.anki_url = anki_url
        self.deck_name = deck_name
        self.model_name = model_name
        self.notifier = notifier
        self._queue = queue.Queue()
        self._client = AnkiConnectClient(anki_url)
        self._setup_complete = False

    def submit(self, lookup_data, screenshot_path: str | None = None):
        self._queue.put(AnkiExportRequest(lookup_data, screenshot_path))

    def stop(self):
        self._queue.put(None)

    def run(self):
        logger.debug("Anki export worker started.")
        while True:
            request = self._queue.get()
            if request is None:
                break
            try:
                self._export(request)
            except Exception:
                logger.exception("Unexpected Anki export failure.")
                self._notify(
                    "Anki export failed",
                    "Unexpected error while exporting to Anki. Check the MeikiKai log for details.",
                    "critical",
                )
            finally:
                if request.screenshot_path:
                    Path(request.screenshot_path).unlink(missing_ok=True)
        logger.debug("Anki export worker stopped.")

    def _export(self, request: AnkiExportRequest):
        payload = build_vocab_card_payload(request.lookup_data)
        if not payload:
            self._notify("Anki export skipped", "No vocabulary entry is visible to export.", "warning")
            return

        try:
            self._sync_config()
            if not self._setup_complete:
                setup_meikikai_note_type(self._client, self.deck_name, self.model_name)
                self._setup_complete = True
            else:
                self._client.create_deck(self.deck_name)

            if note_exists_for_key(self._client, self.model_name, payload.key):
                raise DuplicateNoteError("MeikiKai duplicate key already exists.")

            if request.screenshot_path:
                self._attach_screenshot(payload.fields, request.screenshot_path)

            note = make_note(self.deck_name, self.model_name, payload.fields)
            self._client.add_note(note)
        except DuplicateNoteError:
            self._notify("Already in Anki", f"{payload.expression} is already in Anki.", "duplicate")
            return
        except AnkiConnectionError:
            self._setup_complete = False
            self._notify(
                "Anki unavailable",
                "Open Anki with AnkiConnect enabled, then try Ctrl+Shift+M again.",
                "warning",
            )
            return
        except AnkiModelSetupError as e:
            self._setup_complete = False
            self._notify("Anki setup blocked", str(e), "critical")
            return
        except AnkiApiError as e:
            self._notify("Anki export failed", f"{e.action}: {e.message}", "critical")
            return

        self._notify("Added to Anki", f"{payload.expression} → {self.deck_name}", "success")

    def _attach_screenshot(self, fields: dict[str, str], screenshot_path: str):
        filename = f"meikikai_{uuid4().hex}.png"
        stored_filename = self._client.store_media_file(filename, screenshot_path) or filename
        fields["Screenshot"] = f'<img src="{escape(stored_filename)}">'

    def _sync_config(self):
        if config.anki_connect_url == self.anki_url:
            return

        self.anki_url = config.anki_connect_url
        self._client = AnkiConnectClient(self.anki_url)
        self._setup_complete = False

    def _notify(self, title: str, message: str, level: str):
        self.notifier.message.emit(title, message, level)
