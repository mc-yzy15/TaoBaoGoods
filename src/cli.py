from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Sequence

from src.app import AppRuntimeError, PurchaseApp
from src.config import ConfigValidationError, load_config
from src.paths import DEFAULT_CONFIG_PATH
from src.status import ConsoleStatusSink


def run_gui(config_path: Path) -> int:
    """Launch the Flet GUI (default mode)."""
    try:
        from src.gui import FletGUI
    except ImportError as exc:
        print(f"[错误] Flet GUI 不可用，请安装 flet 依赖: pip install flet\n  ({exc})", file=__import__("sys").stderr)
        return 1

    import flet as ft
    app = FletGUI(config_path)
    ft.app(target=app.build)
    return 0


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TaoBaoGoods Python - 淘宝自动购 深度防检测版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式:
  不带参数           启动 Flet 图形界面（推荐，默认）
  --cli              纯 CLI 模式，使用已有配置文件
  --dry-run          CLI 下验证配置，不打开浏览器
  --purchase-time    CLI 下定时下单，格式: "YYYY-MM-DD HH:MM:SS"
  --help             显示本帮助信息

示例:
  TaoBaoGoods.exe                       # Flet 图形界面
  TaoBaoGoods.exe --cli                 # 纯 CLI 模式
  TaoBaoGoods.exe --cli --dry-run       # CLI dry-run
""",
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to the YAML config file.",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Pure CLI mode - use existing config file, no GUI.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and flow wiring without opening a browser.",
    )
    parser.add_argument(
        "--purchase-time",
        metavar="YYYY-MM-DD HH:MM:SS",
        help="Schedule order placement at a specific time (local time).",
    )
    return parser.parse_args(argv)


def parse_purchase_time(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.strptime(value, TIME_FORMAT)
    except ValueError:
        raise ConfigValidationError(
            f"purchase_time 格式无效: `{value}`，正确格式: {TIME_FORMAT}"
        )


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.cli:
        return run_gui(Path(args.config))

    sink = ConsoleStatusSink()
    try:
        config = load_config(Path(args.config))
        purchase_time = parse_purchase_time(args.purchase_time)
        result = PurchaseApp().run(
            config, sink,
            dry_run=args.dry_run,
            purchase_time=purchase_time
        )
        sink.show_info("完成", result.message)
        return 0
    except (ConfigValidationError, AppRuntimeError) as exc:
        sink.show_error("TaoBaoGoods", str(exc))
        return 1
    finally:
        sink.close()
