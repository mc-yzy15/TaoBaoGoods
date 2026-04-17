from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
import os
import re
import shutil

import yaml


WINDOW_SIZE_PATTERN = re.compile(r"^\d+,\d+$")


class ConfigValidationError(ValueError):
    """Raised when the application config is missing or malformed."""


@dataclass(frozen=True)
class ItemConfig:
    url: str
    quantity: int


@dataclass(frozen=True)
class AppConfig:
    window_size: str
    proxy: str
    driver_path: str
    username: str | None
    password: str | None
    items: tuple[ItemConfig, ...]


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


DEFAULT_CONFIG_TEXT = """# TaoBaoGoods default configuration
window_size: "1280,720"
proxy: ""
driver_path: "chromedriver.exe"
username: ""
password: ""
items:
  - url: "https://example.com/item1"
    quantity: 1
"""


def write_default_config(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DEFAULT_CONFIG_TEXT, encoding="utf-8")


def load_config(path: Path | str, env: Mapping[str, str] | None = None) -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        write_default_config(config_path)

    raw_text = config_path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw_text) or {}
    if not isinstance(data, dict):
        raise ConfigValidationError("配置文件必须是键值映射。")

    window_size = str(data.get("window_size", "1280,720")).strip()
    proxy = str(data.get("proxy", "")).strip()
    driver_path = str(data.get("driver_path", "chromedriver.exe")).strip()
    username = _optional_string(data.get("username"))
    password = _optional_string(data.get("password"))
    items = _parse_items(data.get("items"))

    if not WINDOW_SIZE_PATTERN.match(window_size):
        raise ConfigValidationError("window_size 必须是 `宽,高` 格式，例如 `1280,720`。")
    if not driver_path:
        raise ConfigValidationError("driver_path 不能为空。")

    config = AppConfig(
        window_size=window_size,
        proxy=proxy,
        driver_path=driver_path,
        username=username,
        password=password,
        items=items,
    )

    resolve_credentials(config, env=env)
    return config


def resolve_credentials(
    config: AppConfig,
    env: Mapping[str, str] | None = None,
) -> Credentials | None:
    env_values = env if env is not None else os.environ
    username = _optional_string(env_values.get("TAOBAOGOODS_USERNAME")) or config.username
    password = _optional_string(env_values.get("TAOBAOGOODS_PASSWORD")) or config.password

    if not username and not password:
        return None
    if not username or not password:
        raise ConfigValidationError("用户名和密码必须同时提供，或都留空以便运行时输入。")
    return Credentials(username=username, password=password)


def validate_runtime_prerequisites(config: AppConfig) -> None:
    driver_path = config.driver_path.strip()
    if not driver_path:
        raise ConfigValidationError("driver_path 不能为空。")

    driver_file = Path(driver_path)
    if driver_file.exists():
        return
    if shutil.which(driver_path):
        return
    raise ConfigValidationError(
        f"找不到 ChromeDriver: `{driver_path}`。请提供绝对路径，或确保它位于 PATH 中。"
    )


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_items(items_value: object) -> tuple[ItemConfig, ...]:
    if not isinstance(items_value, list) or not items_value:
        raise ConfigValidationError("items 必须是非空列表。")

    parsed_items: list[ItemConfig] = []
    for index, item in enumerate(items_value, start=1):
        if not isinstance(item, dict):
            raise ConfigValidationError(f"第 {index} 个商品配置必须是对象。")

        url = _optional_string(item.get("url"))
        quantity = item.get("quantity")
        if not url:
            raise ConfigValidationError(f"第 {index} 个商品缺少 url。")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ConfigValidationError(f"第 {index} 个商品的 quantity 必须是正整数。")

        parsed_items.append(ItemConfig(url=url, quantity=quantity))

    return tuple(parsed_items)
