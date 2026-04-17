from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Sequence

from app import AppRuntimeError, PurchaseApp
from config import ConfigValidationError, load_config
from interactive import run_interactive
from paths import DEFAULT_CONFIG_PATH
from status import ConsoleStatusSink, StatusSink


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def build_status_sink(use_tk: bool = True) -> StatusSink:
    if use_tk:
        try:
            from ui import TkStatusSink
            return TkStatusSink()
        except Exception:
            pass
    return ConsoleStatusSink()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TaoBaoGoods Python - 淘宝自动购 深度防检测版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式:
  不带参数           启动交互式TUI配置编辑器（推荐）
  --interactive, -i  同上，显式启动交互模式
  --dry-run         验证配置和流程，不打开浏览器
  --purchase-time   定时下单时间，格式: "YYYY-MM-DD HH:MM:SS"
  --gui             启动GUI模式（Tk窗口，仅状态显示）
  --cli             纯CLI模式，无TUI（使用已有配置文件）
  --help            显示本帮助信息

示例:
  TaoBaoGoods.exe                        # 交互式TUI配置编辑器
  TaoBaoGoods.exe --cli                 # 纯CLI，使用已有配置
  TaoBaoGoods.exe --cli --dry-run        # CLI dry-run
  TaoBaoGoods.exe --gui                  # GUI模式
"""
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to the YAML config file.",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="启动交互式TUI配置编辑器（默认行为）",
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
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Use Tk GUI for status display (no config editor).",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Pure CLI mode - use existing config file, no TUI editor.",
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

    is_tui = not args.gui and not args.cli
    is_dry = args.dry_run
    is_gui = args.gui
    is_cli = args.cli

    if is_tui and not is_dry:
        return run_interactive(Path(args.config))

    if is_gui:
        sink = build_status_sink(use_tk=True)
    else:
        sink = ConsoleStatusSink()

    try:
        config = load_config(Path(args.config))
        purchase_time = parse_purchase_time(args.purchase_time)
        result = PurchaseApp().run(
            config, sink,
            dry_run=is_dry,
            purchase_time=purchase_time
        )
        sink.show_info("完成", result.message)
        return 0
    except (ConfigValidationError, AppRuntimeError) as exc:
        sink.show_error("TaoBaoGoods", str(exc))
        return 1
    finally:
        sink.close()
