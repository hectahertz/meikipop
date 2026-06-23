"""Design tokens for MeikiKai's dark macOS utility UI.

Qt style sheets do not support color variables or OKLCH directly, so tokens are
kept as QSS-compatible RGB/rgba strings and generated from Python.
"""

from dataclasses import dataclass

Rgb = tuple[int, int, int]


def rgba(rgb: Rgb, alpha: int) -> str:
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"


@dataclass(frozen=True)
class DialogTokens:
    font_family: str = "SF Pro Text"
    font_family_qss: str = '"SF Pro Text", "Helvetica Neue", "Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif'
    mono_family_qss: str = '"SF Mono", Menlo, Monaco, monospace'

    neutral_rgb: Rgb = (238, 242, 248)
    accent_rgb: Rgb = (10, 132, 255)
    success_rgb: Rgb = (48, 209, 88)
    warning_rgb: Rgb = (255, 204, 0)
    danger_rgb: Rgb = (255, 69, 58)

    window_bg: str = "#202127"
    text: str = "#eef2f7"
    text_strong: str = "#f4f7fb"
    text_body: str = "#c7cfdd"
    text_muted: str = "#b2bccb"
    text_subtle: str = "#8791a1"
    text_dim: str = "#6f7888"
    status_text: str = "#d3dae6"

    accent: str = "#0a84ff"
    accent_hover: str = "#248fff"
    accent_pressed: str = "#006edb"
    accent_on: str = "#f4f8ff"
    accent_soft_text: str = "#c9e2ff"

    success_text: str = "#9fe8b2"
    warning_text: str = "#e8c762"
    danger_text: str = "#ffd7d4"

    font_size_base: int = 13
    font_size_title: int = 20
    font_size_section: int = 11
    font_size_body: int = 12
    font_size_label: int = 13
    font_size_detail: int = 11
    font_size_badge: int = 10

    title_height: int = 28
    control_height: int = 24

    window_margin_x: int = 18
    window_margin_top: int = 20
    window_margin_bottom: int = 20
    confirm_margin_bottom: int = 20

    panel_radius: int = 12
    inset_panel_radius: int = 10
    control_radius: int = 7
    badge_radius: int = 7

    row_padding_x: int = 14
    row_padding_y: int = 9
    row_gap: int = 18
    action_gap: int = 8
    block_gap: int = 10
    title_gap: int = 14
    prose_gap: int = 8
    prose_panel_gap: int = 12
    footer_gap: int = 18
    section_label_gap: int = 8
    section_gap: int = 16
    inset_panel_padding_x: int = 12
    inset_panel_padding_y: int = 12

    @property
    def panel_bg(self) -> str:
        return rgba(self.neutral_rgb, 12)

    @property
    def panel_border(self) -> str:
        return rgba(self.neutral_rgb, 28)

    @property
    def inset_panel_bg(self) -> str:
        return rgba(self.neutral_rgb, 16)

    @property
    def inset_panel_border(self) -> str:
        return rgba(self.neutral_rgb, 16)

    @property
    def separator(self) -> str:
        return rgba(self.neutral_rgb, 18)

    @property
    def control_bg(self) -> str:
        return rgba(self.neutral_rgb, 14)

    @property
    def control_bg_hover(self) -> str:
        return rgba(self.neutral_rgb, 24)

    @property
    def control_bg_pressed(self) -> str:
        return rgba(self.neutral_rgb, 32)

    @property
    def control_bg_disabled(self) -> str:
        return rgba(self.neutral_rgb, 8)

    @property
    def control_border(self) -> str:
        return rgba(self.neutral_rgb, 36)

    @property
    def control_border_hover(self) -> str:
        return rgba(self.neutral_rgb, 58)

    @property
    def control_border_disabled(self) -> str:
        return rgba(self.neutral_rgb, 18)

    @property
    def control_text_disabled(self) -> str:
        return rgba(self.neutral_rgb, 84)

    @property
    def focus_border(self) -> str:
        return rgba(self.accent_rgb, 170)

    @property
    def accent_border(self) -> str:
        return rgba((123, 193, 255), 160)

    @property
    def accent_tint(self) -> str:
        return rgba(self.accent_rgb, 18)

    @property
    def accent_tint_border(self) -> str:
        return rgba(self.accent_rgb, 64)

    @property
    def keycap_bg(self) -> str:
        return rgba(self.accent_rgb, 24)

    @property
    def keycap_border(self) -> str:
        return rgba(self.accent_rgb, 70)

    @property
    def success_bg(self) -> str:
        return rgba(self.success_rgb, 18)

    @property
    def success_border(self) -> str:
        return rgba(self.success_rgb, 70)

    @property
    def warning_bg(self) -> str:
        return rgba(self.warning_rgb, 14)

    @property
    def warning_border(self) -> str:
        return rgba(self.warning_rgb, 58)

    @property
    def danger_bg(self) -> str:
        return rgba(self.danger_rgb, 18)

    @property
    def danger_bg_hover(self) -> str:
        return rgba(self.danger_rgb, 34)

    @property
    def danger_border(self) -> str:
        return rgba((255, 105, 97), 112)

    @property
    def danger_border_hover(self) -> str:
        return rgba((255, 105, 97), 150)


DIALOG = DialogTokens()
