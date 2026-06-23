"""Small reusable widgets and style helpers for MeikiKai dialogs."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QSizePolicy

from meikikai.gui.design.tokens import DIALOG


def _repolish(widget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def set_button_variant(button: QPushButton, variant: str | None) -> None:
    object_name = {
        "primary": "primaryButton",
        "destructive": "destructiveButton",
        "tertiary": "tertiaryButton",
        None: "",
    }.get(variant)
    if object_name is None:
        raise ValueError(f"Unknown button variant: {variant}")
    button.setObjectName(object_name)
    _repolish(button)


def dialog_title(text: str, *, word_wrap: bool = False) -> QLabel:
    label = QLabel(text)
    label.setObjectName("dialogTitle")
    label.setTextFormat(Qt.TextFormat.PlainText)
    label.setWordWrap(word_wrap)
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    label.setFixedHeight(DIALOG.title_height)
    return label


def body_label(text: str, *, object_name: str = "dialogBody", word_wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(object_name)
    label.setTextFormat(Qt.TextFormat.PlainText)
    label.setWordWrap(word_wrap)
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    return label


def panel_frame(object_name: str = "detailsPanel") -> QFrame:
    panel = QFrame()
    panel.setObjectName(object_name)
    panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    return panel


def separator() -> QFrame:
    line = QFrame()
    line.setObjectName("rowSeparator")
    line.setFixedHeight(1)
    return line
