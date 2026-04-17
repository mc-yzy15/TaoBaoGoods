from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "default.yaml"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
SCREENSHOT_DIR = ARTIFACTS_DIR / "screenshots"


def ensure_runtime_dirs() -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
