# TaoBaoGoods — Agent Guide

## Stack
- **Python** ≥ 3.10, **Flet** (GUI), **Selenium** (browser automation)
- **PyYAML** for config, **selenium-stealth** for anti-detection (CDP injection)

## Entry points
```
main.py                  # python main.py → Flet GUI (default)
main.py --cli            # CLI mode, no GUI
```

## Source layout (`src/`)
| File | Responsibility |
|---|---|
| `gui.py` | Flet GUI (config editor + run status panel) |
| `cli.py` | Argument parsing, routes to Flet GUI or CLI |
| `app.py` | PurchaseApp — orchestrates login → cart → checkout → order |
| `browser_session.py` | Selenium WebDriver wrapper, human-behavior simulation |
| `config.py` | AppConfig/ItemConfig/Credentials data classes, YAML load/save |
| `stealth.py` | CDP-based anti-detection (WebGL, Canvas, navigator forging) |
| `paths.py` | PROJECT_ROOT, CONFIG_DIR, SCREENSHOT_DIR constants |
| `status.py` | StatusSink protocol + ConsoleStatusSink |

## Key patterns
- `StatusSink` protocol: `set_status()` / `show_info()` / `show_error()` / `prompt_text()`
- `BrowserSession` protocol: `login()` / `add_to_cart()` / `checkout()` / `place_order()`
- `FletStatusSink` in `gui.py` updates a Flet page from a background thread
- Config precedence: environment variable > YAML file > runtime input

## Tests
```
pytest tests/
```
