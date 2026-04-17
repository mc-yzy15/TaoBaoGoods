from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from src.browser_session import BrowserActionError, BrowserSession, SeleniumBrowserSession
from src.config import AppConfig, ConfigValidationError, Credentials, resolve_credentials, validate_runtime_prerequisites
from src.status import NullStatusSink, StatusSink


class AppRuntimeError(RuntimeError):
    """Raised when the purchase flow cannot continue."""


@dataclass(frozen=True)
class RunResult:
    success: bool
    message: str
    screenshot_path: Path | None = None


SessionFactory = Callable[[AppConfig], BrowserSession]


class PurchaseApp:
    def __init__(self, session_factory: SessionFactory = SeleniumBrowserSession) -> None:
        self._session_factory = session_factory

    def run(
        self,
        config: AppConfig,
        status_sink: StatusSink | None = None,
        *,
        dry_run: bool = False,
        purchase_time: datetime | None = None,
    ) -> RunResult:
        sink = status_sink or NullStatusSink()
        if dry_run:
            sink.set_status(f"Dry-run: 将处理 {len(config.items)} 个商品。")
            return RunResult(success=True, message="Dry-run 完成，配置和流程结构有效。")

        validate_runtime_prerequisites(config)
        credentials = self._resolve_credentials(config, sink)

        session: BrowserSession | None = None
        try:
            session = self._session_factory(config)
            sink.set_status("正在登录...")
            session.login(credentials.username, credentials.password)

            for item in config.items:
                sink.set_status(f"正在加入购物车: {item.url} x {item.quantity}")
                session.add_to_cart(item.url, item.quantity)

            sink.set_status("正在结算...")
            session.checkout()

            sink.set_status("正在提交订单...")
            session.place_order(target_time=purchase_time)
            sink.set_status("流程执行完成。")
            return RunResult(success=True, message="自动化流程执行完成。")
        except Exception as exc:
            action = exc.action if isinstance(exc, BrowserActionError) else "自动化流程"
            screenshot = session.capture_debug_artifact(action) if session is not None else None
            message = str(exc)
            if screenshot is not None:
                message = f"{message}，已保存截图: {screenshot}"
            raise AppRuntimeError(message) from exc
        finally:
            if session is not None:
                session.close()

    def _resolve_credentials(self, config: AppConfig, sink: StatusSink) -> Credentials:
        credentials = resolve_credentials(config)
        if credentials is not None:
            return credentials

        username = sink.prompt_text("登录凭据", "请输入淘宝用户名：")
        password = sink.prompt_text("登录凭据", "请输入淘宝密码：", secret=True)
        if not username or not password:
            raise ConfigValidationError("缺少登录凭据，且运行时输入未完成。")
        return Credentials(username=username, password=password)
