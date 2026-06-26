import logging
import queue
import threading
from dataclasses import dataclass

from PyQt6.QtCore import QObject, pyqtSignal

from meikikai.tts.shortcuts import (
    ShortcutsTts,
    ShortcutsTtsCommandError,
    ShortcutsTtsEmptyOutputError,
    ShortcutsTtsError,
    ShortcutsTtsInputError,
    ShortcutsTtsMissingShortcutError,
    ShortcutsTtsPlaybackError,
    ShortcutsTtsTimeoutError,
    cleanup_tts_file,
    play_caf,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SpeechPlaybackRequest:
    text: str


class SpeechPlaybackNotifier(QObject):
    message = pyqtSignal(str, str, str)


class ShortcutsSpeechWorker(threading.Thread):
    def __init__(self, notifier: SpeechPlaybackNotifier):
        super().__init__(daemon=True, name="ShortcutsSpeechWorker")
        self.notifier = notifier
        self._queue = queue.Queue()
        self._request_lock = threading.Lock()
        self._request_active = False
        self._stopping = False

    def submit(self, text: str) -> bool:
        spoken_text = (text or "").strip()
        if not spoken_text:
            return False

        with self._request_lock:
            if self._stopping or self._request_active:
                return False
            self._request_active = True

        self._queue.put(SpeechPlaybackRequest(spoken_text))
        return True

    def stop(self):
        with self._request_lock:
            self._stopping = True
        self._queue.put(None)

    def run(self):
        logger.debug("Shortcuts speech worker started.")
        while True:
            request = self._queue.get()
            if request is None:
                break
            try:
                self._speak(request.text)
            except Exception:
                logger.exception("Unexpected Shortcuts speech failure.")
                self._notify(
                    "Speech failed",
                    "Unexpected error while speaking the entry. Check the MeikiKai log for details.",
                    "critical",
                )
            finally:
                with self._request_lock:
                    self._request_active = False
        logger.debug("Shortcuts speech worker stopped.")

    def _speak(self, text: str):
        audio_path = None
        try:
            audio_path = ShortcutsTts().synthesize_to_caf(text)
            play_caf(audio_path)
        except ShortcutsTtsInputError as e:
            self._notify("Speech skipped", str(e), "warning")
        except ShortcutsTtsMissingShortcutError as e:
            self._notify("Shortcut not found", str(e), "warning")
        except ShortcutsTtsEmptyOutputError as e:
            self._notify("No Shortcut audio", str(e), "warning")
        except ShortcutsTtsTimeoutError as e:
            self._notify("Speech timed out", str(e), "warning")
        except ShortcutsTtsPlaybackError as e:
            self._notify("Speech playback failed", str(e), "warning")
        except ShortcutsTtsCommandError as e:
            self._notify("Shortcuts TTS failed", str(e), "warning")
        except ShortcutsTtsError as e:
            self._notify("Shortcuts TTS failed", str(e), "warning")
        finally:
            cleanup_tts_file(audio_path)

    def _notify(self, title: str, message: str, level: str):
        self.notifier.message.emit(title, message, level)
