# AGENTS.md

Repo-specific guidance for coding agents working on MeikiKai.

## Project scope

- MeikiKai is a macOS-only Japanese OCR popup dictionary built with PyQt6.
- Do not add Windows/Linux/cross-platform fallback code unless explicitly requested.
- Keep changes surgical and consistent with the existing local style.
- Preserve user data paths under `~/Library/Application Support/meikikai/` and logs under `~/Library/Logs/MeikiKai/`.

## Working tree safety

- The working tree may contain user changes. Do not revert, overwrite, stage, or commit unrelated files.
- Before committing, stage only files that belong to the requested change and review `git diff --cached`.

## Development commands

- Quick syntax validation:
  - `.venv/bin/python -m py_compile <files>`
- Run from source when needed:
  - `PYTHONPATH=src .venv/bin/python -m meikikai.main`
- Build, sign, install, and reopen the macOS app:
  - `scripts/build_install_macos.sh`

## macOS permissions and packaging notes

- Required macOS permissions include Screen Recording, Accessibility, and Input Monitoring.
- Media auto-pause uses synthetic macOS media key events and requires Accessibility permission.
- After rebuilding or re-signing the app, macOS TCC permissions can become stale. If Accessibility appears checked but media automation fails, remove MeikiKai from Accessibility and add/approve it again, then relaunch.
- The installed app bundle is `/Applications/MeikiKai.app` and bundle identifier is `dev.hectahertz.meikikai`.

## Release guidance

- Project/package/app version is centralized in `src/meikikai/_version.py`.
- Release tags use `meikikai-vX.Y.Z`, for example `meikikai-v1.1.0`.
- Before releasing, bump `__version__`, run targeted syntax validation, commit the version bump, create an annotated tag, and push `main` plus the tag.
- The `Release` GitHub Actions workflow builds the macOS DMG and publishes the GitHub release with generated notes.
- If pushing the tag does not start the workflow, dispatch it manually:
  - `gh workflow run release.yml --ref main -f tag=meikikai-vX.Y.Z`
  - `gh run watch <run-id> --exit-status`
- After the workflow completes, verify the release and uploaded DMG:
  - `gh release view meikikai-vX.Y.Z --json tagName,name,url,isDraft,isPrerelease,assets,publishedAt`

## Validation guidance

- Prefer targeted validation over full builds for small edits.
- Use the full build/install script only when changing packaging, app startup behavior, bundled resources, permissions, or when explicitly requested.
