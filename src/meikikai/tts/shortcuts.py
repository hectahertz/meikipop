# meikikai/tts/shortcuts.py
import logging
import os
import subprocess
import tempfile
from pathlib import Path

from meikikai.config.config import DEFAULT_SHORTCUTS_TTS_SHORTCUT_NAME
from meikikai.utils.paths import paths

logger = logging.getLogger(__name__)

SHORTCUTS_BINARY = "/usr/bin/shortcuts"
AFPLAY_BINARY = "/usr/bin/afplay"
AFCONVERT_BINARY = "/usr/bin/afconvert"
DEFAULT_SHORTCUTS_TTS_TIMEOUT_SECONDS = 30.0
DEFAULT_SHORTCUTS_LIST_TIMEOUT_SECONDS = 2.5
DEFAULT_AFPLAY_TIMEOUT_SECONDS = 45.0
DEFAULT_AFCONVERT_TIMEOUT_SECONDS = 20.0


class ShortcutsTtsError(RuntimeError):
    """Base error for Shortcuts TTS failures."""


class ShortcutsTtsInputError(ShortcutsTtsError):
    """The TTS request cannot be run as provided."""


class ShortcutsTtsUnavailableError(ShortcutsTtsError):
    """The macOS Shortcuts or playback command is unavailable."""


class ShortcutsTtsMissingShortcutError(ShortcutsTtsError):
    """The configured Shortcut could not be found."""


class ShortcutsTtsTimeoutError(ShortcutsTtsError):
    """The Shortcuts TTS command timed out."""


class ShortcutsTtsCommandError(ShortcutsTtsError):
    """The Shortcuts TTS command exited unsuccessfully."""

    def __init__(self, message: str, returncode: int, stdout: str = "", stderr: str = ""):
        super().__init__(message)
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class ShortcutsTtsEmptyOutputError(ShortcutsTtsError):
    """The Shortcut completed but did not produce audio."""


class ShortcutsTtsConversionError(ShortcutsTtsError):
    """Generated audio could not be converted for Anki."""


class ShortcutsTtsPlaybackError(ShortcutsTtsError):
    """Generated audio could not be played."""


class ShortcutsTts:
    """Generate CAF speech audio with the fixed MeikiKai macOS Shortcut."""

    def __init__(self, timeout_seconds: float = DEFAULT_SHORTCUTS_TTS_TIMEOUT_SECONDS):
        self.shortcut_name = DEFAULT_SHORTCUTS_TTS_SHORTCUT_NAME
        self.timeout_seconds = timeout_seconds

    def synthesize_to_caf(self, text: str) -> Path:
        spoken_text = text.strip()
        if not spoken_text:
            raise ShortcutsTtsInputError("No text was provided for speech.")

        output_path = _make_temp_caf_path()
        command = [
            SHORTCUTS_BINARY,
            "run",
            self.shortcut_name,
            "-i",
            "-",
            "-o",
            str(output_path),
        ]

        try:
            result = subprocess.run(
                command,
                input=spoken_text,
                capture_output=True,
                check=False,
                encoding="utf-8",
                text=True,
                timeout=self.timeout_seconds,
            )
        except FileNotFoundError as e:
            cleanup_tts_file(output_path)
            raise ShortcutsTtsUnavailableError(
                f"macOS Shortcuts was not found at {SHORTCUTS_BINARY}."
            ) from e
        except subprocess.TimeoutExpired as e:
            cleanup_tts_file(output_path)
            logger.warning("Shortcuts TTS timed out for shortcut '%s'.", self.shortcut_name)
            raise ShortcutsTtsTimeoutError(
                f"Shortcut '{self.shortcut_name}' timed out after {self.timeout_seconds:g} seconds."
            ) from e
        except OSError as e:
            cleanup_tts_file(output_path)
            raise ShortcutsTtsUnavailableError(f"Could not run macOS Shortcuts: {e}") from e

        if result.returncode != 0:
            cleanup_tts_file(output_path)
            detail = _command_detail(result.stdout, result.stderr)
            logger.warning(
                "Shortcuts TTS failed for shortcut '%s' with exit code %s. stderr=%r stdout=%r",
                self.shortcut_name,
                result.returncode,
                _truncate(result.stderr),
                _truncate(result.stdout),
            )
            if _looks_like_missing_shortcut(detail):
                raise ShortcutsTtsMissingShortcutError(
                    f"Shortcut '{self.shortcut_name}' was not found. Create it in Shortcuts, then try again."
                )
            raise ShortcutsTtsCommandError(
                f"Shortcut '{self.shortcut_name}' failed: {detail or 'unknown Shortcuts error'}",
                result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )

        if not _is_non_empty_file(output_path):
            cleanup_tts_file(output_path)
            raise ShortcutsTtsEmptyOutputError(
                "The Shortcut returned no audio. It should Receive Text, then end with "
                "Make Spoken Audio from Shortcut Input. Do not add Stop and Output after it."
            )

        return output_path


def shortcut_exists(timeout_seconds: float = DEFAULT_SHORTCUTS_LIST_TIMEOUT_SECONDS) -> bool:
    """Return whether macOS Shortcuts has the fixed MeikiKai Shortcut."""
    name = DEFAULT_SHORTCUTS_TTS_SHORTCUT_NAME
    try:
        result = subprocess.run(
            [SHORTCUTS_BINARY, "list"],
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError as e:
        raise ShortcutsTtsUnavailableError(
            f"macOS Shortcuts was not found at {SHORTCUTS_BINARY}."
        ) from e
    except subprocess.TimeoutExpired as e:
        logger.warning("Timed out listing macOS Shortcuts while checking for '%s'.", name)
        raise ShortcutsTtsTimeoutError(
            f"Timed out checking Shortcuts for '{name}' after {timeout_seconds:g} seconds."
        ) from e
    except OSError as e:
        raise ShortcutsTtsUnavailableError(f"Could not list macOS Shortcuts: {e}") from e

    if result.returncode != 0:
        detail = _command_detail(result.stdout, result.stderr)
        logger.warning(
            "Failed to list macOS Shortcuts while checking for '%s'. exit=%s stderr=%r stdout=%r",
            name,
            result.returncode,
            _truncate(result.stderr),
            _truncate(result.stdout),
        )
        raise ShortcutsTtsCommandError(
            f"Could not list Shortcuts: {detail or 'unknown Shortcuts error'}",
            result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    return any(line.strip() == name for line in result.stdout.splitlines())


def convert_caf_to_m4a(caf_path: str | Path, timeout_seconds: float = DEFAULT_AFCONVERT_TIMEOUT_SECONDS) -> Path:
    input_path = Path(caf_path)
    if not _is_non_empty_file(input_path):
        raise ShortcutsTtsConversionError("Generated CAF audio is missing or empty.")

    output_path = _make_temp_m4a_path()
    command = [
        AFCONVERT_BINARY,
        "-f",
        "m4af",
        "-d",
        "aac",
        "-q",
        "127",
        str(input_path),
        str(output_path),
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            encoding="utf-8",
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError as e:
        cleanup_tts_file(output_path)
        raise ShortcutsTtsUnavailableError(f"macOS audio converter was not found at {AFCONVERT_BINARY}.") from e
    except subprocess.TimeoutExpired as e:
        cleanup_tts_file(output_path)
        raise ShortcutsTtsConversionError(f"Audio conversion timed out after {timeout_seconds:g} seconds.") from e
    except OSError as e:
        cleanup_tts_file(output_path)
        raise ShortcutsTtsConversionError(f"Could not convert generated audio: {e}") from e

    if result.returncode != 0:
        cleanup_tts_file(output_path)
        detail = _command_detail(result.stdout, result.stderr)
        logger.warning(
            "afconvert failed with exit code %s. stderr=%r stdout=%r",
            result.returncode,
            _truncate(result.stderr),
            _truncate(result.stdout),
        )
        raise ShortcutsTtsConversionError(f"Audio conversion failed: {detail or 'unknown afconvert error'}")

    if not _is_non_empty_file(output_path):
        cleanup_tts_file(output_path)
        raise ShortcutsTtsConversionError("Audio conversion produced no M4A output.")

    return output_path


def play_caf(audio_path: str | Path, timeout_seconds: float = DEFAULT_AFPLAY_TIMEOUT_SECONDS) -> None:
    path = Path(audio_path)
    if not _is_non_empty_file(path):
        raise ShortcutsTtsPlaybackError("Generated audio is missing or empty.")

    try:
        result = subprocess.run(
            [AFPLAY_BINARY, str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
            encoding="utf-8",
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError as e:
        raise ShortcutsTtsUnavailableError(f"macOS audio player was not found at {AFPLAY_BINARY}.") from e
    except subprocess.TimeoutExpired as e:
        raise ShortcutsTtsPlaybackError(f"Audio playback timed out after {timeout_seconds:g} seconds.") from e
    except OSError as e:
        raise ShortcutsTtsPlaybackError(f"Could not play generated audio: {e}") from e

    if result.returncode != 0:
        detail = (result.stderr or "").strip()
        logger.warning("afplay failed with exit code %s. stderr=%r", result.returncode, _truncate(detail))
        raise ShortcutsTtsPlaybackError(f"Audio playback failed: {detail or 'unknown afplay error'}")


def cleanup_tts_file(audio_path: str | Path | None) -> None:
    if not audio_path:
        return
    try:
        Path(audio_path).unlink(missing_ok=True)
    except OSError:
        logger.debug("Failed to remove temporary TTS audio file '%s'.", audio_path, exc_info=True)


def _make_temp_caf_path() -> Path:
    return _make_temp_audio_path(".caf")


def _make_temp_m4a_path() -> Path:
    return _make_temp_audio_path(".m4a")


def _make_temp_audio_path(suffix: str) -> Path:
    fd, temp_path = tempfile.mkstemp(prefix="meikikai_tts_", suffix=suffix, dir=paths.cache_dir)
    os.close(fd)
    path = Path(temp_path)
    path.unlink(missing_ok=True)
    return path


def _is_non_empty_file(path: Path) -> bool:
    try:
        return path.is_file() and path.stat().st_size > 0
    except OSError:
        return False


def _command_detail(stdout: str, stderr: str) -> str:
    return (stderr or stdout or "").strip()


def _looks_like_missing_shortcut(message: str) -> bool:
    text = message.lower()
    return any(marker in text for marker in (
        "shortcut could not be found",
        "shortcut couldn't be found",
        "shortcut not found",
        "could not find shortcut",
        "couldn't find shortcut",
        "not found",
    ))


def _truncate(text: str, limit: int = 500) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return f"{text[:limit]}…"
