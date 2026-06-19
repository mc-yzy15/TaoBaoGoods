# TaoBaoGoods — Agent Guide

## Stack
- **Python ≥ 3.10**, **Flet** (GUI), **Selenium** (browser automation)
- **PyYAML** for config, **selenium-stealth** for CDP-based anti-detection
- **Nuitka** (standalone + onefile) for cross-platform builds

## Entry points
```
main.py                  # python main.py → Flet GUI (default)
python -m src            # same as above, via src/__main__.py
main.py --cli            # CLI mode, no GUI
main.py --cli --dry-run  # validate config, open no browser
```

Installable CLI:
```
pip install -e . && taobaogoods     # via pyproject.toml [project.scripts]
```

## Scripts (Windows)
```
.\scripts\init.ps1       # create .venv + pip install -e .
.\scripts\start.ps1      # run main.py from .venv (passes --cli, --dry-run etc.)
.\start.bat              # cmd shim → scripts\start.ps1
```

## Source layout (`src/`)
| File | Responsibility |
|---|---|
| `cli.py` | arg parsing, routes to Flet GUI or CLI mode |
| `gui.py` | Flet GUI (config editor + run status panel) |
| `app.py` | PurchaseApp — orchestrates login → cart → checkout → order |
| `browser_session.py` | Selenium WebDriver wrapper, human-behavior simulation |
| `config.py` | AppConfig/ItemConfig/Credentials data classes, YAML load/save |
| `stealth.py` | CDP-based anti-detection (WebGL, Canvas, navigator forging) — largest file |
| `paths.py` | PROJECT_ROOT, CONFIG_DIR, SCREENSHOT_DIR constants |
| `status.py` | StatusSink protocol + ConsoleStatusSink |

## Key patterns
- `StatusSink` protocol: `set_status()` / `show_info()` / `show_error()` / `prompt_text()`
- `BrowserSession` protocol: `login()` / `add_to_cart()` / `checkout()` / `place_order()` — in tests, inject a `FakeSession` via `session_factory` kwarg
- `FletStatusSink` in `gui.py` updates Flet UI from a background thread
- Config precedence: `TAOBAOGOODS_USERNAME` / `TAOBAOGOODS_PASSWORD` env var > YAML file > runtime input
- `PurchaseApp` accepts `session_factory: SessionFactory = SeleniumBrowserSession` — injectable for tests
- `DRY_RUN` skips browser session entirely; `purchase_time` triggers timed order placement

## Tests
```
python -m unittest discover -s tests -p "test_*.py" -v
```
- Uses **unittest**, not pytest
- Test files add `src/` to `sys.path` and import modules directly (not `src.config`) — be aware if refactoring
- `FakeSession` / `FakeStatusSink` test doubles in `test_app.py`
- Temporary directories and fake driver files for config tests
- CI runs tests on every push to `dev` (build-per-push.yml) and on release builds

## Build & CI
- CI builds Nuitka standalone one-file executables for win/linux/macos (x86_64 + arm64)
- Release flow: tag `v*` on `master` → build-release.yml → GitHub Release
- Nightly builds on `master`, branch builds on `dev`
- Assets directory (`assets/icon.ico`, `assets/icon.png`, `assets/icon.icns`) expected for icon embedding

## Environment quirks
- `chromedriver.exe` must be in PATH or specified as absolute path in config
- Slider CAPTCHA triggers on login — agent cannot automate it; requires manual intervention
- Screenshots saved to `artifacts/screenshots/` on error
- The `docs/README.md` is the PyPI readme (not the root `README.MD`)
