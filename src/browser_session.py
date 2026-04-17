from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol
import re

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import AppConfig
from paths import SCREENSHOT_DIR, ensure_runtime_dirs


SELECTORS = {
    "login_url": "https://login.taobao.com",
    "cart_url": "https://cart.taobao.com/cart.htm",
    "username": (By.ID, "fm-login-id"),
    "password": (By.ID, "fm-login-password"),
    "add_to_cart": (By.ID, "J_AddToCart"),
    "select_all": (By.ID, "J_SelectAllCbx1"),
    "checkout": (By.ID, "J_Go"),
    "submit_order": (By.ID, "J_Go"),
}


class BrowserError(RuntimeError):
    """Base browser error."""


@dataclass
class BrowserActionError(BrowserError):
    action: str
    detail: str

    def __str__(self) -> str:
        return f"{self.action} 失败: {self.detail}"


class BrowserSession(Protocol):
    def login(self, username: str, password: str) -> None:
        ...

    def add_to_cart(self, url: str, quantity: int) -> None:
        ...

    def checkout(self) -> None:
        ...

    def place_order(self) -> None:
        ...

    def capture_debug_artifact(self, action: str) -> Path | None:
        ...

    def close(self) -> None:
        ...


class SeleniumBrowserSession:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._driver = self._build_driver(config)

    def login(self, username: str, password: str) -> None:
        def _perform() -> None:
            self._driver.get(SELECTORS["login_url"])
            username_input = self._wait_for(SELECTORS["username"])
            password_input = self._wait_for(SELECTORS["password"])
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            WebDriverWait(self._driver, 10).until(
                lambda driver: "login.taobao.com" not in driver.current_url
            )

        self._run_action("登录", _perform)

    def add_to_cart(self, url: str, quantity: int) -> None:
        def _perform() -> None:
            self._driver.get(url)
            button = self._wait_clickable(SELECTORS["add_to_cart"])
            for _ in range(quantity):
                button.click()

        self._run_action(f"商品加购 ({url})", _perform)

    def checkout(self) -> None:
        def _perform() -> None:
            self._driver.get(SELECTORS["cart_url"])
            self._wait_clickable(SELECTORS["select_all"]).click()
            self._wait_clickable(SELECTORS["checkout"]).click()

        self._run_action("结算", _perform)

    def place_order(self) -> None:
        def _perform() -> None:
            self._wait_clickable(SELECTORS["submit_order"]).click()

        self._run_action("提交订单", _perform)

    def capture_debug_artifact(self, action: str) -> Path | None:
        if self._driver is None:
            return None

        ensure_runtime_dirs()
        safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", action).strip("_") or "browser_error"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        screenshot_path = SCREENSHOT_DIR / f"{safe_name}-{timestamp}.png"
        try:
            self._driver.save_screenshot(str(screenshot_path))
        except WebDriverException:
            return None
        return screenshot_path

    def close(self) -> None:
        if self._driver is None:
            return
        try:
            self._driver.quit()
        finally:
            self._driver = None

    def _build_driver(self, config: AppConfig) -> webdriver.Chrome:
        options = Options()
        options.add_argument(f"--window-size={config.window_size}")
        if config.proxy:
            options.add_argument(f"--proxy-server={config.proxy}")

        return webdriver.Chrome(service=Service(config.driver_path), options=options)

    def _wait_for(self, locator: tuple[str, str]):
        return WebDriverWait(self._driver, 10).until(EC.presence_of_element_located(locator))

    def _wait_clickable(self, locator: tuple[str, str]):
        return WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(locator))

    def _run_action(self, action: str, operation) -> None:
        try:
            operation()
        except Exception as exc:  # pragma: no cover - exercised in manual browser runs.
            raise BrowserActionError(action=action, detail=str(exc)) from exc
