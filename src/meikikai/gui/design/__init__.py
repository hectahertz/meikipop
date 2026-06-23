"""Shared UI design helpers for MeikiKai's PyQt dialogs."""

from meikikai.gui.design.styles import apply_dialog_style, dialog_stylesheet
from meikikai.gui.design.tokens import DIALOG, rgba
from meikikai.gui.design.widgets import (
    body_label,
    dialog_title,
    panel_frame,
    separator,
    set_button_variant,
)

__all__ = [
    "DIALOG",
    "apply_dialog_style",
    "body_label",
    "dialog_stylesheet",
    "dialog_title",
    "panel_frame",
    "rgba",
    "separator",
    "set_button_variant",
]
