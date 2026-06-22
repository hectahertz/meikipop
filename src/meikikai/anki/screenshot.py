# meikikai/anki/screenshot.py
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


SCREENCAPTURE_PATH = "/usr/sbin/screencapture"


def capture_interactive_png() -> Optional[str]:
    """Open the native macOS crop UI and return a PNG path, or None if no image is captured."""
    fd, path_str = tempfile.mkstemp(prefix="meikikai-anki-", suffix=".png")
    os.close(fd)
    path = Path(path_str)
    path.unlink(missing_ok=True)

    result = subprocess.run(
        [SCREENCAPTURE_PATH, "-i", "-x", "-t", "png", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        path.unlink(missing_ok=True)
        logger.debug("Interactive screenshot capture canceled or failed with exit code %s.", result.returncode)
        return None

    if not path.exists() or path.stat().st_size == 0:
        path.unlink(missing_ok=True)
        logger.debug("Interactive screenshot capture produced no image.")
        return None

    return str(path)
