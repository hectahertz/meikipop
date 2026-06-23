# MeikiKai design system

MeikiKai is a macOS menu bar utility for reading Japanese text from the screen. Design serves the task: fast lookup, low distraction, and enough polish that permission and setup flows feel trustworthy.

## Scene

A reader is watching Japanese media or a visual novel on a Mac, often in a dim room, and glances at MeikiKai only long enough to understand a word or complete setup.

## Direction

- Native macOS utility, custom enough to support dark overlays.
- Dark only for now.
- Restrained color: tinted neutrals plus macOS blue for primary action and focus.
- Compact but not cramped. Dialogs should feel calm and predictable.
- The dictionary popup may stay denser than dialogs because it is a transient reading aid.

## Implementation

Shared dialog styling lives in:

- `src/meikikai/gui/design/tokens.py`: colors, typography, radii, spacing.
- `src/meikikai/gui/design/styles.py`: generated QSS for dialogs.
- `src/meikikai/gui/design/widgets.py`: small helpers for titles, separators, panels, and button variants.

Qt style sheets do not support CSS variables or OKLCH, so token values are stored as QSS-compatible RGB and rgba strings. When changing color direction, choose colors in OKLCH first, then convert the final values to Qt-compatible strings.

## Tokens

### Typography

- UI family: SF Pro Text, then common macOS and Japanese fallbacks.
- Base size: 13 px.
- Dialog title: 20 px, 750 weight.
- Body: 12 px, brighter than helper text for setup and confirmation copy.
- Section labels and helper text: 11 px. Section labels are muted so setting titles carry the local hierarchy.
- Avoid display fonts in controls, labels, settings, and status text.

### Color roles

- Window: dark neutral surface.
- Panel: faint raised neutral layer with a low-contrast border.
- Text: strong, default, body, muted, subtle, disabled.
- Accent: macOS blue for primary actions, focus, keycaps, and progress.
- Semantic: success, warning, destructive.

Do not use pure `#000` or `#fff`. Use tinted near-black and near-white values.

### Shape and spacing

- Dialog margin: 18 px horizontal, 20 px vertical.
- Panel radius: 12 px.
- Inset panel radius: 10 px.
- Control radius: 7 px.
- Setting row padding: 14 px horizontal, 9 px vertical.
- Setting row gap: 18 px.
- Title-to-content gap: 14 px.
- Prose block gap: 8 px.
- Prose-to-panel gap: 12 px.
- Footer/action separation: 18 px above action rows.
- Section gap: 16 px. Section label-to-panel gap: 8 px.
- Inset panel padding: 12 px horizontal and vertical.
- Status and detail panels use a faint inset fill with a near-zero border; avoid hard boxed contrast in setup and confirmation flows.

## Components

### Dialogs

Call `apply_dialog_style(self)` in each dialog constructor. Use object names from the shared stylesheet rather than local QSS blocks.

Common object names:

- `dialogTitle`
- `dialogBody`, `bodyText`, `confirmBody`, `messageBody`
- `settingsPanel`, `statusPanel`, `detailsPanel`
- `rowSeparator`
- `settingTitle`, `settingDescription`
- `statusBadgeReady`, `statusBadgeWarning`
- `progressText`, `detailTitle`, `detailText`, `pathText`, `messageDetail`

### Buttons

Use `set_button_variant(button, variant)`:

- `primary`: main action only.
- `destructive`: removal, quit, or irreversible actions.
- `tertiary`: link-style supporting action, such as notices or documentation.
- `None`: default secondary button.

Primary actions should be sparse. Settings should have one primary action, Save. Inline management actions stay secondary unless they complete the current dialog's main task. In a maintenance flow, reinstall/update and uninstall sit in the same action row, while notices move to a tertiary link. Single dismiss actions such as OK should normally stay secondary. Action rows use the shared 8 px gap between buttons. Do not put separator lines above footer buttons; use the shared footer gap instead.

### Panels

Use panels for grouped settings, component status, and install details. Settings panels may keep a clearer grouped outline; status and detail panels should feel quieter, using subtle inset fill and subdued key labels so the value text scans first. Avoid nested panels unless the inner panel carries a different information type.

### Badges

Badges are short state labels only, such as Ready, Reload, Missing. They should not replace explanatory body text.

## Popup guidance

The popup has different constraints from dialogs: cursor anchoring, Japanese typography, and dense dictionary content. Keep it separate until dialog consistency is stable. When updating it later, map its colors and typography to shared tokens without forcing settings-row or dialog-panel patterns onto it.
