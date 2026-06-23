#!/usr/bin/env python3
"""Render MeikiKai dialog screenshots and a contact sheet for UI review."""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from PyQt6.QtCore import Qt  # noqa: E402
from PyQt6.QtWidgets import QApplication, QDialog  # noqa: E402

from meikikai.gui import screen_ai_setup_dialog as screen_ai_dialogs  # noqa: E402
from meikikai.gui import settings_dialog as settings_dialogs  # noqa: E402
from meikikai.gui.screen_ai_setup_dialog import (  # noqa: E402
    ScreenAiDownloadConfirmDialog,
    ScreenAiMessageDialog,
    ScreenAiSetupDialog,
    ScreenAiUninstallConfirmDialog,
)
from meikikai.gui.settings_dialog import SettingsDialog  # noqa: E402
from meikikai.ocr.providers.chrome_screen_ai.component import (  # noqa: E402
    CIPD_SOURCE_LABEL,
    CIPD_REQUESTED_VERSION,
    ScreenAiComponentStatus,
)

OUTPUT_DIR = ROOT / "design" / "dialog-screenshots"
CONTACT_SHEET = ROOT / "design" / "dialog-contact-sheet.png"
SAMPLE_INSTALL_DIR = Path.home() / "Library" / "Application Support" / "meikikai" / "screen_ai"
SAMPLE_COMPONENT_DIR = SAMPLE_INSTALL_DIR / "resources"


class DummyEvent:
    def set(self):
        pass


class DummySharedState:
    screenshot_trigger_event = DummyEvent()


class DummyPopupWindow:
    shared_state = DummySharedState()

    def reapply_settings(self):
        pass


class DummyTrayIcon:
    def reapply_settings(self):
        pass


class DummyOcrProcessor:
    def __init__(self, available: bool = False, last_error: str | None = None):
        self.available = available
        self.last_error = last_error

    def is_backend_available(self) -> bool:
        return self.available

    def unload_ocr_backend(self, reason: str):
        pass

    def reload_ocr_backend(self) -> bool:
        return self.available


@dataclass(frozen=True)
class DialogSample:
    name: str
    factory: Callable[[], QDialog]
    status: ScreenAiComponentStatus


class PatchedScreenAiStatus:
    def __init__(self, status: ScreenAiComponentStatus):
        self.status = status
        self.original_screen_status = screen_ai_dialogs.get_screen_ai_status
        self.original_settings_status = settings_dialogs.get_screen_ai_status
        self.original_install_dir = screen_ai_dialogs.screen_ai_install_dir

    def __enter__(self):
        screen_ai_dialogs.get_screen_ai_status = lambda: self.status
        settings_dialogs.get_screen_ai_status = lambda: self.status
        screen_ai_dialogs.screen_ai_install_dir = lambda: SAMPLE_INSTALL_DIR

    def __exit__(self, exc_type, exc, traceback):
        screen_ai_dialogs.get_screen_ai_status = self.original_screen_status
        settings_dialogs.get_screen_ai_status = self.original_settings_status
        screen_ai_dialogs.screen_ai_install_dir = self.original_install_dir


def missing_status() -> ScreenAiComponentStatus:
    return ScreenAiComponentStatus(
        installed=False,
        install_dir=SAMPLE_INSTALL_DIR,
        package="chromium/third_party/screen-ai/mac-arm64",
    )


def installed_status() -> ScreenAiComponentStatus:
    return ScreenAiComponentStatus(
        installed=True,
        install_dir=SAMPLE_INSTALL_DIR,
        component_dir=SAMPLE_COMPONENT_DIR,
        source=CIPD_SOURCE_LABEL,
        package="chromium/third_party/screen-ai/mac-arm64",
        requested_version=CIPD_REQUESTED_VERSION,
        resolved_version="sample-review-build",
        instance_id="sample-instance-id",
        notices_path=SAMPLE_INSTALL_DIR / "THIRD_PARTY_LICENSES",
        readme_path=SAMPLE_INSTALL_DIR / "README.md",
    )


def installed_not_loaded_status() -> ScreenAiComponentStatus:
    return installed_status()


def samples() -> list[DialogSample]:
    missing = missing_status()
    installed = installed_status()
    installed_not_loaded = installed_not_loaded_status()

    return [
        DialogSample(
            "01-settings-missing",
            lambda: SettingsDialog(DummyPopupWindow(), DummyTrayIcon(), DummyOcrProcessor(False)),
            missing,
        ),
        DialogSample(
            "02-setup-required-missing",
            lambda: ScreenAiSetupDialog(
                DummyOcrProcessor(False),
                tray_icon=DummyTrayIcon(),
                setup_required=True,
            ),
            missing,
        ),
        DialogSample(
            "03-setup-installed-not-loaded",
            lambda: ScreenAiSetupDialog(
                DummyOcrProcessor(False, last_error="Restart MeikiKai before OCR resumes."),
                tray_icon=DummyTrayIcon(),
                setup_required=False,
            ),
            installed_not_loaded,
        ),
        DialogSample(
            "04-download-confirm",
            lambda: ScreenAiDownloadConfirmDialog(installed=False),
            missing,
        ),
        DialogSample(
            "05-reinstall-confirm",
            lambda: ScreenAiDownloadConfirmDialog(installed=True),
            installed,
        ),
        DialogSample(
            "06-uninstall-confirm",
            lambda: ScreenAiUninstallConfirmDialog(installed),
            installed,
        ),
        DialogSample(
            "07-message-simple",
            lambda: ScreenAiMessageDialog(
                "Third-party notices unavailable",
                "No THIRD_PARTY_LICENSES or README.md file was found in the installed Chrome Screen AI component.",
            ),
            installed,
        ),
        DialogSample(
            "08-message-detail",
            lambda: ScreenAiMessageDialog(
                "Chrome Screen AI setup failed",
                "MeikiKai could not download or install Chrome Screen AI.",
                "Network request timed out while contacting chrome-infra-packages.appspot.com.",
            ),
            missing,
        ),
    ]


def render_dialog(app: QApplication, sample: DialogSample, output_dir: Path) -> Path:
    with PatchedScreenAiStatus(sample.status):
        dialog = sample.factory()
        dialog.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen, True)
        dialog.show()
        app.processEvents()
        pixmap = dialog.grab()
        output = output_dir / f"{sample.name}.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        pixmap.save(str(output))
        dialog.close()
        dialog.deleteLater()
        app.processEvents()
        return output


def _font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def make_contact_sheet(images: list[Path], output: Path, columns: int = 3) -> None:
    loaded = [(path, Image.open(path).convert("RGBA")) for path in images]
    if not loaded:
        raise RuntimeError("No dialog screenshots were rendered.")

    label_font = _font(14, bold=True)
    meta_font = _font(11)
    tile_bg = (54, 60, 72, 255)
    page_bg = tile_bg
    text = (238, 242, 247, 255)
    muted = (170, 179, 194, 255)

    gutter = 16
    margin = 20
    label_h = 34
    inner_pad = 8
    tile_sizes = [max(image.width, image.height) + inner_pad * 2 for _, image in loaded]
    column_count = min(columns, len(loaded))
    columns_data: list[list[tuple[int, Path, Image.Image, int]]] = [[] for _ in range(column_count)]
    column_heights = [0] * column_count

    for index, ((path, image), tile_size) in enumerate(zip(loaded, tile_sizes)):
        column = min(range(column_count), key=lambda col: column_heights[col])
        columns_data[column].append((index, path, image, tile_size))
        column_heights[column] += label_h + tile_size + gutter

    column_widths = [
        max((tile_size for _, _, _, tile_size in column), default=0)
        for column in columns_data
    ]
    sheet_w = margin * 2 + sum(column_widths) + gutter * (column_count - 1)
    sheet_h = margin * 2 + max(column_heights) - gutter

    sheet = Image.new("RGBA", (sheet_w, sheet_h), page_bg)
    draw = ImageDraw.Draw(sheet)

    x = margin
    for column_width, column in zip(column_widths, columns_data):
        y = margin
        for index, path, image, tile_size in column:
            tile_x = x + (column_width - tile_size) // 2
            label = path.stem.removeprefix(f"{index + 1:02d}-").replace("-", " ").title()
            draw.text((tile_x, y), label, fill=text, font=label_font)
            draw.text((tile_x, y + 16), f"{image.width} × {image.height}px", fill=muted, font=meta_font)

            tile_y = y + label_h
            draw.rectangle((tile_x, tile_y, tile_x + tile_size, tile_y + tile_size), fill=tile_bg)
            image_x = tile_x + (tile_size - image.width) // 2
            image_y = tile_y + (tile_size - image.height) // 2
            sheet.alpha_composite(image, (image_x, image_y))
            y += label_h + tile_size + gutter
        x += column_width + gutter

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render MeikiKai dialogs and a review contact sheet.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--contact-sheet", type=Path, default=CONTACT_SHEET)
    parser.add_argument("--columns", type=int, default=3)
    args = parser.parse_args()

    app = QApplication.instance() or QApplication([])
    rendered = [render_dialog(app, sample, args.output_dir) for sample in samples()]
    make_contact_sheet(rendered, args.contact_sheet, columns=args.columns)

    for image in rendered:
        print(image.relative_to(ROOT))
    print(args.contact_sheet.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
