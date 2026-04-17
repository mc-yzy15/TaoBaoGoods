from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from app import AppRuntimeError, PurchaseApp
from config import ConfigValidationError, load_config
from paths import DEFAULT_CONFIG_PATH
from status import ConsoleStatusSink, StatusSink
from ui import TkStatusSink


def build_status_sink(dry_run: bool) -> StatusSink:
    if dry_run:
        return ConsoleStatusSink()
    try:
        return TkStatusSink()
    except Exception:
        return ConsoleStatusSink()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TaoBaoGoods Python mainline")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to the YAML config file. Defaults to python_Version/config/default.yaml.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and flow wiring without opening a browser.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    sink = build_status_sink(args.dry_run)
    try:
        config = load_config(Path(args.config))
        result = PurchaseApp().run(config, sink, dry_run=args.dry_run)
        sink.show_info("完成", result.message)
        return 0
    except (ConfigValidationError, AppRuntimeError) as exc:
        sink.show_error("TaoBaoGoods", str(exc))
        return 1
    finally:
        sink.close()
