from pathlib import Path
import sys


PROJECT_SRC = Path(__file__).resolve().parent / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from cli import main


if __name__ == "__main__":
    raise SystemExit(main())
