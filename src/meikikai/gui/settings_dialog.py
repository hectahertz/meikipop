# meikikai/gui/settings_dialog.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QDialog, QFormLayout, QComboBox,
                             QSpinBox, QVBoxLayout, QGroupBox, QDialogButtonBox,
                             QLabel, QDoubleSpinBox, QSizePolicy)

from meikikai.config.config import config, APP_NAME
from meikikai.gui.popup import Popup
from meikikai.ocr.ocr import OcrProcessor
from meikikai.utils.paths import paths


class SettingsDialog(QDialog):
    def __init__(self, ocr_processor: OcrProcessor, popup_window: Popup, tray_icon, parent=None):
        super().__init__(parent)
        self.ocr_processor = ocr_processor
        self.popup_window = popup_window
        self.tray_icon = tray_icon

        self.setWindowTitle(f"{APP_NAME} Settings")
        self.setWindowIcon(QIcon(paths.get_resource_path('app_icon.icns')))
        self.setMinimumWidth(400)

        # Keep track of all form layouts to unify their spacing later.
        self.form_layouts = []

        main_layout = QVBoxLayout(self)

        # --- Group 1: Core Settings ---
        core_group = QGroupBox("Core Settings")
        core_layout = QFormLayout()
        self.form_layouts.append(core_layout)

        self.max_lookup_spin = QSpinBox()
        self.max_lookup_spin.setRange(5, 100)
        self.max_lookup_spin.setValue(config.max_lookup_length)
        core_layout.addRow("Max Lookup Length:", self.max_lookup_spin)

        core_group.setLayout(core_layout)
        main_layout.addWidget(core_group)

        # --- Group 2: Scanning ---
        scan_group = QGroupBox("Scanning")
        scan_layout = QFormLayout()
        self.form_layouts.append(scan_layout)

        self.auto_scan_interval_spin_label = QLabel("Scan Interval (Cooldown):")
        self.auto_scan_interval_spin = QDoubleSpinBox()
        self.auto_scan_interval_spin.setRange(0.0, 60.0)
        self.auto_scan_interval_spin.setDecimals(1)
        self.auto_scan_interval_spin.setSingleStep(0.1)
        self.auto_scan_interval_spin.setValue(config.auto_scan_interval_seconds)
        self.auto_scan_interval_spin.setSuffix(" s")
        self.auto_scan_interval_spin.setToolTip(
            "Minimum time between OCR scans\nCan reduce system load, but worsens perceived latency")
        scan_layout.addRow(self.auto_scan_interval_spin_label, self.auto_scan_interval_spin)

        scan_group.setLayout(scan_layout)
        main_layout.addWidget(scan_group)

        # --- Group 3: Popup Behavior ---
        behavior_group = QGroupBox("Popup Behavior")
        behavior_layout = QFormLayout()
        self.form_layouts.append(behavior_layout)

        self.popup_position_combo = QComboBox()
        self.popup_position_combo.addItems(["Flip Both", "Flip Vertically", "Flip Horizontally", "Visual Novel Mode"])
        self.popup_mode_map = {
            "Flip Both": "flip_both",
            "Flip Vertically": "flip_vertically",
            "Flip Horizontally": "flip_horizontally",
            "Visual Novel Mode": "visual_novel_mode"
        }
        current_friendly_name = next(
            (k for k, v in self.popup_mode_map.items() if v == config.popup_position_mode), "Visual Novel Mode"
        )
        self.popup_position_combo.setCurrentText(current_friendly_name)
        self._set_expanding(self.popup_position_combo)
        behavior_layout.addRow("Position Mode:", self.popup_position_combo)

        behavior_group.setLayout(behavior_layout)
        main_layout.addWidget(behavior_group)
        main_layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save_and_accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)

        self._finalize_layout_styling()

    def _set_expanding(self, widget):
        """Helper to let a widget expand horizontally."""
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _finalize_layout_styling(self):
        """Sets all label columns to the same width to align controls."""
        max_label_width = 0

        for layout in self.form_layouts:
            for i in range(layout.rowCount()):
                item = layout.itemAt(i, QFormLayout.ItemRole.LabelRole)
                if item and item.widget():
                    max_label_width = max(max_label_width, item.widget().sizeHint().width())

        max_label_width += 5

        for layout in self.form_layouts:
            layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
            layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.setHorizontalSpacing(15)

            for i in range(layout.rowCount()):
                item = layout.itemAt(i, QFormLayout.ItemRole.LabelRole)
                if item and item.widget():
                    item.widget().setMinimumWidth(max_label_width)

    def save_and_accept(self):
        config.max_lookup_length = self.max_lookup_spin.value()
        config.auto_scan_interval_seconds = self.auto_scan_interval_spin.value()

        selected_friendly_name = self.popup_position_combo.currentText()
        config.popup_position_mode = self.popup_mode_map.get(selected_friendly_name, "visual_novel_mode")
        config.save()

        self.popup_window.reapply_settings()
        self.tray_icon.reapply_settings()
        self.ocr_processor.shared_state.screenshot_trigger_event.set()

        self.accept()
