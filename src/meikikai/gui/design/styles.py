"""Shared Qt style sheets for MeikiKai dialogs."""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget

from meikikai.gui.design.tokens import DIALOG


def dialog_stylesheet(extra: str = "") -> str:
    t = DIALOG
    stylesheet = f"""
        QDialog {{
            background-color: {t.window_bg};
            color: {t.text};
            font-family: {t.font_family_qss};
            font-size: {t.font_size_base}px;
        }}
        QLabel#dialogTitle {{
            color: {t.text_strong};
            font-size: {t.font_size_title}px;
            font-weight: 750;
        }}
        QLabel#sectionLabel {{
            color: {t.text_muted};
            font-size: {t.font_size_section}px;
            font-weight: 700;
            letter-spacing: 0.2px;
        }}
        QLabel#settingTitle {{
            color: {t.text};
            font-size: {t.font_size_label}px;
            font-weight: 650;
        }}
        QLabel#dialogBody,
        QLabel#bodyText,
        QLabel#confirmBody,
        QLabel#messageBody {{
            color: {t.text_body};
            font-size: {t.font_size_body}px;
            line-height: 145%;
        }}
        QLabel#settingDescription,
        QLabel#infoText {{
            color: {t.text_muted};
            font-size: {t.font_size_detail}px;
            line-height: 132%;
        }}
        QLabel#infoShortcut {{
            background-color: {t.keycap_bg};
            border: 1px solid {t.keycap_border};
            border-radius: 6px;
            color: {t.accent_soft_text};
            font-size: {t.font_size_detail}px;
            font-weight: 700;
            padding: 3px 7px;
        }}
        QLabel#bulletMarker {{
            color: {t.text_subtle};
            font-size: 14px;
            font-weight: 800;
        }}
        QLabel#detailTitle {{
            color: {t.text};
            font-size: {t.font_size_detail}px;
            font-weight: 700;
        }}
        QLabel#detailText {{
            color: {t.text_subtle};
            font-size: {t.font_size_detail}px;
        }}
        QLabel#pathText,
        QLabel#messageDetail {{
            color: {t.text_muted};
            font-family: {t.mono_family_qss};
            font-size: {t.font_size_detail}px;
        }}
        QLabel#progressText {{
            background-color: {t.accent_tint};
            border: 1px solid {t.accent_tint_border};
            border-radius: {t.inset_panel_radius}px;
            color: {t.accent_soft_text};
            font-size: {t.font_size_body}px;
            font-weight: 650;
            line-height: 145%;
            padding: 8px 10px;
        }}
        QLabel#statusTitle {{
            color: {t.text_dim};
            font-size: {t.font_size_detail}px;
            font-weight: 650;
        }}
        QLabel#statusValue {{
            color: {t.status_text};
            font-size: {t.font_size_body}px;
            font-weight: 600;
        }}
        QLabel#statusBadgeReady,
        QLabel#statusBadgeWarning {{
            border-radius: {t.badge_radius}px;
            font-size: {t.font_size_badge}px;
            font-weight: 750;
            padding: 3px 7px;
        }}
        QLabel#statusBadgeReady {{
            background-color: {t.success_bg};
            border: 1px solid {t.success_border};
            color: {t.success_text};
        }}
        QLabel#statusBadgeWarning {{
            background-color: {t.warning_bg};
            border: 1px solid {t.warning_border};
            color: {t.warning_text};
        }}
        QFrame#settingsPanel {{
            background-color: {t.panel_bg};
            border: 1px solid {t.panel_border};
            border-radius: {t.panel_radius}px;
        }}
        QFrame#statusPanel {{
            background-color: {t.inset_panel_bg};
            border: 1px solid {t.inset_panel_border};
            border-radius: {t.panel_radius}px;
        }}
        QFrame#detailsPanel {{
            background-color: {t.inset_panel_bg};
            border: 1px solid {t.inset_panel_border};
            border-radius: {t.inset_panel_radius}px;
        }}
        QFrame#rowSeparator {{
            background-color: {t.separator};
            border: none;
        }}
        QSpinBox,
        QDoubleSpinBox,
        QLineEdit,
        QComboBox {{
            background-color: {t.control_bg};
            border: 1px solid {t.control_border};
            border-radius: {t.control_radius}px;
            color: {t.text};
            min-height: {t.control_height}px;
            padding: 2px 8px;
            selection-background-color: {t.accent};
            selection-color: {t.accent_on};
        }}
        QComboBox {{
            padding-right: 22px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {t.window_bg};
            border: 1px solid {t.control_border};
            color: {t.text};
            outline: none;
            selection-background-color: {t.accent};
            selection-color: {t.accent_on};
        }}
        QSpinBox:focus,
        QDoubleSpinBox:focus,
        QLineEdit:focus,
        QComboBox:focus {{
            border-color: {t.focus_border};
        }}
        QSpinBox:disabled,
        QDoubleSpinBox:disabled,
        QLineEdit:disabled,
        QComboBox:disabled {{
            background-color: {t.control_bg_disabled};
            border-color: {t.control_border_disabled};
            color: {t.control_text_disabled};
        }}
        QPushButton {{
            background-color: {t.control_bg};
            border: 1px solid {t.control_border};
            border-radius: {t.control_radius}px;
            color: {t.text_body};
            font-weight: 550;
            min-height: {t.control_height}px;
            padding: 3px 10px;
        }}
        QPushButton:hover {{
            background-color: {t.control_bg_hover};
            border-color: {t.control_border_hover};
        }}
        QPushButton:pressed {{
            background-color: {t.control_bg_pressed};
        }}
        QPushButton:disabled {{
            background-color: {t.control_bg_disabled};
            border-color: {t.control_border_disabled};
            color: {t.control_text_disabled};
        }}
        QPushButton#primaryButton {{
            background-color: {t.accent};
            border-color: {t.accent_border};
            color: {t.accent_on};
            font-weight: 650;
        }}
        QPushButton#primaryButton:hover {{
            background-color: {t.accent_hover};
        }}
        QPushButton#primaryButton:pressed {{
            background-color: {t.accent_pressed};
        }}
        QPushButton#primaryButton:disabled {{
            background-color: {t.control_bg_disabled};
            border-color: {t.control_border_disabled};
            color: {t.control_text_disabled};
        }}
        QPushButton#destructiveButton {{
            background-color: {t.danger_bg};
            border-color: {t.danger_border};
            color: {t.danger_text};
        }}
        QPushButton#destructiveButton:hover {{
            background-color: {t.danger_bg_hover};
            border-color: {t.danger_border_hover};
            color: {t.text_strong};
        }}
        QPushButton#destructiveButton:disabled {{
            background-color: {t.control_bg_disabled};
            border-color: {t.control_border_disabled};
            color: {t.control_text_disabled};
        }}
        QPushButton#tertiaryButton {{
            background-color: transparent;
            border: none;
            color: {t.accent_soft_text};
            font-weight: 550;
            min-height: 20px;
            padding: 2px 0;
            text-align: left;
        }}
        QPushButton#tertiaryButton:hover {{
            background-color: transparent;
            border: none;
            color: {t.accent_on};
            text-decoration: underline;
        }}
        QPushButton#tertiaryButton:pressed {{
            background-color: transparent;
            color: {t.text_body};
        }}
        QPushButton#tertiaryButton:disabled {{
            background-color: transparent;
            border: none;
            color: {t.control_text_disabled};
        }}
    """
    if extra:
        stylesheet = f"{stylesheet}\n{extra}"
    return stylesheet


def apply_dialog_style(widget: QWidget, extra: str = "") -> None:
    base_font = QFont(DIALOG.font_family)
    base_font.setPixelSize(DIALOG.font_size_base)
    widget.setFont(base_font)
    widget.setStyleSheet(dialog_stylesheet(extra))
