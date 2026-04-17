from __future__ import annotations

import random
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

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


TAOBAO_SELECTORS = {
    "login_url": "https://login.taobao.com",
    "cart_url": "https://cart.taobao.com/cart.htm",
    "username": (By.ID, "fm-login-id"),
    "password": (By.ID, "fm-login-password"),
    "login_submit": (By.ID, "login-form"),
    "add_to_cart": (By.CSS_SELECTOR, ".J_AddToCart"),
    "add_to_cart_alt": (By.ID, "J_AddToCart"),
    "select_all": (By.ID, "J_SelectAllCbx1"),
    "checkout": (By.ID, "J_Go"),
    "submit_order": (By.CSS_SELECTOR, ".go-buy-wrap .go-btn"),
    "submit_order_alt": (By.ID, "J_Go"),
    "captcha": (By.CSS_SELECTOR, "#captcha-container, .nc_wrapper"),
    "login_success": (By.CSS_SELECTOR, ".site-nav-user, .user-info"),
}


class BrowserError(RuntimeError):
    pass


@dataclass
class BrowserActionError(BrowserError):
    action: str
    detail: str

    def __str__(self) -> str:
        return f"{self.action} 失败: {detail}"


class BrowserSession(Protocol):
    def login(self, username: str, password: str) -> None: ...
    def add_to_cart(self, url: str, quantity: int) -> None: ...
    def checkout(self) -> None: ...
    def place_order(self, target_time: datetime | None = None) -> None: ...
    def capture_debug_artifact(self, action: str) -> Path | None: ...
    def close(self) -> None: ...


class SeleniumBrowserSession:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._driver = self._build_driver(config)
        self._stealth()

    def login(self, username: str, password: str) -> None:
        def _perform() -> None:
            self._driver.get(SELECTORS["login_url"])
            time.sleep(random.uniform(1.0, 2.5))
            username_input = self._wait_for(SELECTORS["username"])
            self._human_type(username_input, username)
            time.sleep(random.uniform(0.3, 0.8))
            password_input = self._wait_for(SELECTORS["password"])
            self._human_type(password_input, password)
            time.sleep(random.uniform(0.2, 0.5))
            password_input.send_keys(Keys.RETURN)
            time.sleep(random.uniform(2.0, 4.0))
            if self._is_element_visible(SELECTORS["captcha"], timeout=3):
                raise BrowserActionError(
                    action="登录",
                    detail="检测到滑块验证码，请手动在浏览器中完成验证后重试。"
                )
            WebDriverWait(self._driver, 15).until(
                lambda d: "login.taobao.com" not in d.current_url
            )

        self._run_action("登录", _perform)

    def add_to_cart(self, url: str, quantity: int) -> None:
        def _perform() -> None:
            self._driver.get(url)
            time.sleep(random.uniform(2.0, 4.0))
            self._scroll_random()
            time.sleep(random.uniform(0.5, 1.5))
            button = self._find_add_to_cart_button()
            if button is None:
                raise BrowserActionError(
                    action=f"商品加购 ({url})",
                    detail="未找到加购按钮，页面结构可能已更新。"
                )
            for _ in range(quantity):
                self._human_click(button)
                time.sleep(random.uniform(0.5, 1.2))

        self._run_action(f"商品加购 ({url})", _perform)

    def checkout(self) -> None:
        def _perform() -> None:
            self._driver.get(SELECTORS["cart_url"])
            time.sleep(random.uniform(2.0, 3.5))
            self._scroll_random()
            time.sleep(random.uniform(0.5, 1.0))
            select_all = self._wait_clickable(SELECTORS["select_all"])
            self._human_click(select_all)
            time.sleep(random.uniform(0.5, 1.0))
            checkout_btn = self._wait_clickable(SELECTORS["checkout"])
            self._human_click(checkout_btn)

        self._run_action("结算", _perform)

    def place_order(self, target_time: datetime | None = None) -> None:
        def _perform() -> None:
            if target_time is not None:
                self._wait_until_target_time(target_time)
            submit_btn = self._find_submit_button()
            if submit_btn is None:
                raise BrowserActionError(
                    action="提交订单",
                    detail="未找到提交订单按钮，页面结构可能已更新。"
                )
            self._human_click(submit_btn)
            time.sleep(1.0)

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
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        if config.proxy:
            options.add_argument(f"--proxy-server={config.proxy}")
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        )
        options.add_argument(f"--user-agent={user_agent}")
        return webdriver.Chrome(service=Service(config.driver_path), options=options)

    def _stealth(self) -> None:
        self._driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => 'granted'})});
            """
        })

    def _human_type(self, element, text: str) -> None:
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        element.send_keys(Keys.TAB)

    def _human_click(self, element) -> None:
        size = element.size
        offset_x = random.uniform(size["width"] * 0.2, size["width"] * 0.8)
        offset_y = random.uniform(size["height"] * 0.2, size["height"] * 0.8)
        from selenium.webdriver.common.action_chains import ActionChains
        chain = ActionChains(self._driver)
        chain.move_to_element_with_offset(element, offset_x, offset_y)
        chain.pause(random.uniform(0.1, 0.3))
        chain.click()
        chain.perform()

    def _scroll_random(self) -> None:
        from selenium.webdriver.common.action_chains import ActionChains
        chain = ActionChains(self._driver)
        scroll_count = random.randint(1, 3)
        for _ in range(scroll_count):
            chain.scroll(0, random.randint(200, 600))
            chain.pause(random.uniform(0.3, 0.7))
        chain.perform()

    def _wait_until_target_time(self, target: datetime) -> None:
        while True:
            now = datetime.now()
            diff = (target - now).total_seconds()
            if diff <= 0:
                break
            if diff > 60:
                time.sleep(30)
            elif diff > 10:
                time.sleep(5)
            elif diff > 1:
                time.sleep(0.5)
            else:
                time.sleep(0.01)
        time.sleep(random.uniform(0.05, 0.15))

    def _find_add_to_cart_button(self):
        for selector in [SELECTORS["add_to_cart"], SELECTORS["add_to_cart_alt"]]:
            try:
                return WebDriverWait(self._driver, 3).until(
                    EC.element_to_be_clickable(selector)
                )
            except Exception:
                continue
        return None

    def _find_submit_button(self):
        for selector in [SELECTORS["submit_order"], SELECTORS["submit_order_alt"]]:
            try:
                return WebDriverWait(self._driver, 3).until(
                    EC.element_to_be_clickable(selector)
                )
            except Exception:
                continue
        return None

    def _is_element_visible(self, locator, timeout: int = 0):
        try:
            WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def _wait_for(self, locator):
        return WebDriverWait(self._driver, 15).until(EC.presence_of_element_located(locator))

    def _wait_clickable(self, locator):
        return WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable(locator))

    def _run_action(self, action: str, operation) -> None:
        try:
            operation()
        except BrowserActionError:
            raise
        except Exception as exc:
            raise BrowserActionError(action=action, detail=str(exc)) from exc


SELECTORS = TAOBAO_SELECTORS
