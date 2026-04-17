from __future__ import annotations

import os
import sys
from pathlib import Path

from config import (
    DEFAULT_CONFIG_TEXT,
    AppConfig,
    ConfigValidationError,
    ItemConfig,
    load_config,
    write_default_config,
)

_HAVE_READLINE = False
try:
    import readline
    _HAVE_READLINE = True
except ImportError:
    pass

if sys.platform == "win32":
    import msvcrt
else:
    import tty
    import termios


C_BLACK = "\033[30m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_MAGENTA = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_BRIGHT = "\033[1m"
C_DIM = "\033[2m"
C_RESET = "\033[0m"
C_BG_BLUE = "\033[44m"
C_BG_MAGENTA = "\033[45m"
C_REVERSE = "\033[7m"


def clear_screen() -> None:
    if sys.platform == "win32":
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def move_cursor(row: int, col: int) -> None:
    sys.stdout.write(f"\033[{row+1};{col+1}H")
    sys.stdout.flush()


def erase_line() -> None:
    sys.stdout.write("\033[2K")
    sys.stdout.flush()


def erase_down() -> None:
    sys.stdout.write("\033[J")
    sys.stdout.flush()


def hide_cursor() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor() -> None:
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def bold(text: str) -> str:
    return f"{C_BRIGHT}{text}{C_RESET}"


def color(fg: str, text: str) -> str:
    return f"{fg}{text}{C_RESET}"


def prompt_input(prompt_str: str, default: str = "", secret: bool = False, width: int = 60) -> str:
    prompt_str = prompt_str.strip()
    if not default:
        full_prompt = f"{C_CYAN}{prompt_str}{C_RESET}: "
    else:
        full_prompt = f"{C_CYAN}{prompt_str}{C_RESET} [{C_DIM}{default}{C_RESET}]: "

    sys.stdout.write(full_prompt)
    sys.stdout.flush()

    if secret:
        import getpass
        value = getpass.getpass("") or default
    else:
        if _HAVE_READLINE:
            try:
                readline.set_startup_hook()
            except Exception:
                pass
        try:
            value = sys.stdin.readline()
        except EOFError:
            value = ""
        value = value.rstrip("\r\n") or default

    return value.strip()


def confirm(prompt_str: str, default: bool = False) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        sys.stdout.write(f"{C_YELLOW}{prompt_str} {suffix}{C_RESET}: ")
        sys.stdout.flush()
        try:
            line = sys.stdin.readline()
        except EOFError:
            line = ""
        line = line.strip().lower()
        if line in ("y", "yes"):
            return True
        elif line in ("n", "no"):
            return False
        elif line == "":
            return default
        else:
            sys.stdout.write(f"{C_RED}请输入 y 或 n{C_RESET}\n")


def draw_box(title: str, width: int = 78, top: bool = True) -> None:
    if top:
        sys.stdout.write(f"{C_BRIGHT}{C_BLUE}┌{'─' * (width - 2)}┐{C_RESET}\n")
    else:
        sys.stdout.write(f"{C_BRIGHT}{C_BLUE}└{'─' * (width - 2)}┘{C_RESET}\n")


def draw_divider(width: int = 78) -> None:
    sys.stdout.write(f"{C_BRIGHT}{C_BLUE}├{'─' * (width - 2)}┤{C_RESET}\n")


def print_header(title: str, width: int = 78) -> None:
    clear_screen()
    hide_cursor()
    sys.stdout.write(f"{C_BRIGHT}{C_BG_BLUE}{'':═^{width - 4}}{C_RESET}\n")
    sys.stdout.write(f"{C_BRIGHT}{C_BG_BLUE}  {title:<{width - 6}}  {C_RESET}\n")
    sys.stdout.write(f"{C_BRIGHT}{C_BG_BLUE}{'':═^{width - 4}}{C_RESET}\n")
    sys.stdout.flush()


def print_menu_item(idx: int, label: str, hotkey: str = "", selected: bool = False, indent: int = 4) -> None:
    prefix = f"{C_BRIGHT}{C_CYAN}> {C_RESET}" if selected else f"{' ' * (indent - 2)}  "
    if hotkey:
        label = label.replace(hotkey, f"{C_BRIGHT}{C_YELLOW}{hotkey}{C_RESET}", 1)
    sys.stdout.write(f"{prefix}{label}\n")


def get_key() -> str:
    if sys.platform == "win32":
        ch = msvcrt.getch()
        if ch in (b'\xe0',):
            ch2 = msvcrt.getch()
            if ch2 == b'H':
                return "UP"
            elif ch2 == b'P':
                return "DOWN"
            elif ch2 == b'M':
                return "RIGHT"
            elif ch2 == b'K':
                return "LEFT"
            return ""
        elif ch == b'\r':
            return "ENTER"
        elif ch == b'\x1b':
            return "ESC"
        try:
            return ch.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                next1 = sys.stdin.read(1)
                next2 = sys.stdin.read(1)
                if next1 == "[":
                    if next2 == "A":
                        return "UP"
                    elif next2 == "B":
                        return "DOWN"
                    elif next2 == "C":
                        return "RIGHT"
                    elif next2 == "D":
                        return "LEFT"
                return "ESC"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class InteractiveConfigEditor:
    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path
        self._config: AppConfig | None = None
        self._username = ""
        self._password = ""
        self._items: list[ItemConfig] = []
        self._window_size = "1280,720"
        self._proxy = ""
        self._driver_path = "chromedriver.exe"
        self._changed = False
        self._selected_index = 0
        self._done = False
        self._width = 78

    def run(self) -> None:
        try:
            self._load_or_create_config()
            self._main_loop()
        finally:
            show_cursor()

    def _load_or_create_config(self) -> None:
        if self._config_path.exists():
            try:
                self._config = load_config(self._config_path)
                self._window_size = self._config.window_size
                self._proxy = self._config.proxy
                self._driver_path = self._config.driver_path
                self._username = self._config.username or ""
                self._password = self._config.password or ""
                self._items = list(self._config.items)
            except Exception:
                self._config = None
                self._window_size = "1280,720"
                self._proxy = ""
                self._driver_path = "chromedriver.exe"
                self._username = ""
                self._password = ""
                self._items = []
        else:
            write_default_config(self._config_path)
            self._window_size = "1280,720"
            self._proxy = ""
            self._driver_path = "chromedriver.exe"
            self._username = ""
            self._password = ""
            self._items = []

    def _save_config(self) -> bool:
        if not self._driver_path.strip():
            print(f"{C_RED}[错误] ChromeDriver 路径不能为空{C_RESET}")
            return False

        parts = self._window_size.split(",")
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            print(f"{C_RED}[错误] 窗口大小格式无效，请使用 宽,高 格式（如 1280,720）{C_RESET}")
            return False

        item_lines = []
        for item in self._items:
            item_lines.append(f"  - url: \"{item.url}\"")
            item_lines.append(f"    quantity: {item.quantity}")

        items_text = "\n".join(item_lines) if item_lines else "  - url: \"\"\n    quantity: 1"

        config_text = f"""# TaoBaoGoods configuration
window_size: "{self._window_size}"
proxy: "{self._proxy}"
driver_path: "{self._driver_path}"
username: "{self._username}"
password: "{self._password}"
items:
{items_text}
"""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            self._config_path.write_text(config_text, encoding="utf-8")
            self._changed = False
            return True
        except Exception as e:
            print(f"{C_RED}[错误] 保存配置失败: {e}{C_RESET}")
            return False

    def _main_loop(self) -> None:
        self._selected_index = 0
        self._done = False

        while not self._done:
            self._render()
            key = get_key()
            self._handle_key(key)

    def _render(self) -> None:
        clear_screen()
        hide_cursor()

        sys.stdout.write(f"{C_BRIGHT}{C_BG_BLUE}{'':═^{self._width - 4}}{C_RESET}\n")
        sys.stdout.write(f"{C_BRIGHT}{C_BG_BLUE}  TaoBaoGoods 配置编辑器  (纯终端交互版)  {'':>14}{C_RESET}\n")
        sys.stdout.write(f"{C_BRIGHT}{C_BG_BLUE}{'':═^{self._width - 4}}{C_RESET}\n\n")

        items = self._build_menu_items()
        for i, item in enumerate(items):
            selected = i == self._selected_index
            self._render_menu_item(item, selected, i)

        self._render_status_bar()

    def _build_menu_items(self) -> list[dict]:
        return [
            {"type": "header", "text": "─── 基础设置 ───"},
            {"type": "item", "id": "window_size", "text": f"窗口大小      {C_CYAN}{self._window_size}{C_RESET}", "hotkey": "W"},
            {"type": "item", "id": "proxy", "text": f"代理服务器    {C_CYAN}{self._proxy or '(无)'}{C_RESET}", "hotkey": "P"},
            {"type": "item", "id": "driver_path", "text": f"ChromeDriver  {C_CYAN}{self._driver_path}{C_RESET}", "hotkey": "D"},
            {"type": "header", "text": "─── 登录凭据 ───"},
            {"type": "item", "id": "username", "text": f"用户名        {C_CYAN}{self._username or '(未设置)'}{C_RESET}", "hotkey": "U"},
            {"type": "item", "id": "password", "text": f"密码          {C_CYAN}{'******' if self._password else '(未设置)'}{C_RESET}", "hotkey": "L"},
            {"type": "header", "text": "─── 商品列表 ───"},
            {"type": "item", "id": "add_item", "text": f"添加商品  (当前 {C_CYAN}{len(self._items)}{C_RESET} 个)", "hotkey": "A"},
            {"type": "item", "id": "edit_item", "text": f"编辑商品", "hotkey": "E", "disabled": len(self._items) == 0},
            {"type": "item", "id": "remove_item", "text": f"删除商品", "hotkey": "R", "disabled": len(self._items) == 0},
            {"type": "header", "text": "─── 运行 ───"},
            {"type": "item", "id": "save", "text": f"保存配置  {'(已保存)' if not self._changed else f'{C_YELLOW}*有未保存更改{C_RESET}'}", "hotkey": "S"},
            {"type": "item", "id": "run", "text": "立即运行 (包含自动保存)", "hotkey": "G"},
            {"type": "item", "id": "dry_run", "text": "Dry-Run 模式 (仅验证配置)", "hotkey": "T"},
            {"type": "item", "id": "quit", "text": "退出", "hotkey": "Q"},
        ]

    def _render_menu_item(self, item: dict, selected: bool, idx: int) -> None:
        indent = 2
        if item["type"] == "header":
            sys.stdout.write(f"\n{C_BRIGHT}{C_MAGENTA}  {item['text']}{C_RESET}\n")
            return

        disabled = item.get("disabled", False)
        prefix = f"{C_BRIGHT}{C_GREEN} >>{C_RESET} " if selected else "     "
        text = item["text"]

        hotkey = item.get("hotkey", "")
        if hotkey and hotkey in text:
            text = text.replace(hotkey, f"{C_BRIGHT}{C_YELLOW}[{hotkey}]{C_RESET}", 1)

        if disabled:
            sys.stdout.write(f"     {C_DIM}{text}{C_RESET}\n")
        else:
            sys.stdout.write(f"{prefix}{text}\n")

    def _render_status_bar(self) -> None:
        sys.stdout.write(f"\n{C_DIM}{'─' * self._width}{C_RESET}\n")
        status = "↑↓/数字键 选择   Enter/双击 确定   ESC/Q 退出"
        if self._changed:
            status += f"   {C_YELLOW}* 有未保存更改{C_RESET}"
        sys.stdout.write(f"  {C_DIM}{status}{C_RESET}\n")
        sys.stdout.flush()

    def _handle_key(self, key: str) -> None:
        items = self._build_menu_items()
        selectable = [i for i, item in enumerate(items) if item["type"] == "item" and not item.get("disabled", False)]

        if key in ("UP", "w", "W", "\x1b[A"):
            current = selectable.index(self._selected_index) if self._selected_index in selectable else 0
            current = max(0, current - 1)
            self._selected_index = selectable[current]
        elif key in ("DOWN", "s", "S", "\x1b[B"):
            current = selectable.index(self._selected_index) if self._selected_index in selectable else 0
            current = min(len(selectable) - 1, current + 1)
            self._selected_index = selectable[current]
        elif key in ("\r", "ENTER", " ", "\n"):
            self._activate_selected()
        elif key.isdigit():
            idx = int(key) - 1
            if 0 <= idx < len(selectable):
                self._selected_index = selectable[idx]
                self._activate_selected()
        elif key in ("q", "Q", "\x1b", "ESC"):
            self._done = True
        else:
            hotkey_map = {
                "w": "window_size", "W": "window_size",
                "p": "proxy", "P": "proxy",
                "d": "driver_path", "D": "driver_path",
                "u": "username", "U": "username",
                "l": "password", "L": "password",
                "a": "add_item", "A": "add_item",
                "e": "edit_item", "E": "edit_item",
                "r": "remove_item", "R": "remove_item",
                "s": "save", "S": "save",
                "g": "run", "G": "run",
                "t": "dry_run", "T": "dry_run",
                "q": "quit", "Q": "quit",
            }
            item_id = hotkey_map.get(key)
            if item_id:
                for i, item in enumerate(items):
                    if item.get("id") == item_id:
                        self._selected_index = i
                        break
                self._activate_selected()

    def _activate_selected(self) -> None:
        items = self._build_menu_items()
        item = items[self._selected_index]
        if item["type"] != "item":
            return

        item_id = item.get("id", "")
        if item_id == "window_size":
            self._edit_window_size()
        elif item_id == "proxy":
            self._edit_proxy()
        elif item_id == "driver_path":
            self._edit_driver_path()
        elif item_id == "username":
            self._edit_username()
        elif item_id == "password":
            self._edit_password()
        elif item_id == "add_item":
            self._add_item()
        elif item_id == "edit_item":
            self._edit_item()
        elif item_id == "remove_item":
            self._remove_item()
        elif item_id == "save":
            self._do_save()
        elif item_id == "run":
            self._do_run(dry_run=False)
        elif item_id == "dry_run":
            self._do_run(dry_run=True)
        elif item_id == "quit":
            if self._changed:
                if confirm("有未保存的更改，确认退出？", default=False):
                    self._done = True
            else:
                self._done = True

    def _edit_window_size(self) -> None:
        clear_screen()
        show_cursor()
        print(f"\n{C_BRIGHT}── 窗口大小 ──{C_RESET}\n")
        print(f"当前值: {C_CYAN}{self._window_size}{C_RESET}")
        print(f"格式: 宽,高  例如: {C_CYAN}1280,720{C_RESET}  或  {C_CYAN}1920,1080{C_RESET}\n")

        value = prompt_input("输入窗口大小", default=self._window_size)
        if value.strip():
            parts = value.strip().split(",")
            if len(parts) == 2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                self._window_size = f"{parts[0].strip()},{parts[1].strip()}"
                self._changed = True
            else:
                print(f"{C_RED}格式错误，请使用 宽,高 格式（如 1280,720）{C_RESET}")
                try:
                    sys.stdin.readline()
                except Exception:
                    pass

    def _edit_proxy(self) -> None:
        clear_screen()
        show_cursor()
        print(f"\n{C_BRIGHT}── 代理服务器 ──{C_RESET}\n")
        print(f"当前值: {C_CYAN}{self._proxy or '(无)'}{C_RESET}")
        print(f"格式: 协议://IP:端口  例如: {C_CYAN}http://127.0.0.1:7890{C_RESET}\n")

        value = prompt_input("输入代理地址", default=self._proxy)
        self._proxy = value.strip()
        self._changed = True

    def _edit_driver_path(self) -> None:
        clear_screen()
        show_cursor()
        print(f"\n{C_BRIGHT}── ChromeDriver 路径 ──{C_RESET}\n")
        print(f"当前值: {C_CYAN}{self._driver_path}{C_RESET}")
        print(f"可以是绝对路径，或只写文件名（如 {C_CYAN}chromedriver.exe{C_RESET}）\n")

        value = prompt_input("输入ChromeDriver路径", default=self._driver_path)
        if value.strip():
            self._driver_path = value.strip()
            self._changed = True

    def _edit_username(self) -> None:
        clear_screen()
        show_cursor()
        print(f"\n{C_BRIGHT}── 用户名 ──{C_RESET}\n")
        print(f"当前值: {C_CYAN}{self._username or '(未设置)'}{C_RESET}\n")

        value = prompt_input("输入淘宝用户名", default=self._username)
        self._username = value.strip()
        self._changed = True

    def _edit_password(self) -> None:
        clear_screen()
        show_cursor()
        print(f"\n{C_BRIGHT}── 密码 ──{C_RESET}\n")
        print(f"当前值: {C_CYAN}{'******' if self._password else '(未设置)'}{C_RESET}\n")

        value = prompt_input("输入淘宝密码", default="", secret=True)
        if value:
            self._password = value
            self._changed = True

    def _add_item(self) -> None:
        clear_screen()
        show_cursor()
        print(f"\n{C_BRIGHT}── 添加商品 ──{C_RESET}\n")

        url = prompt_input("商品链接")
        if not url.strip():
            print(f"{C_RED}链接不能为空{C_RESET}")
            try:
                sys.stdin.readline()
            except Exception:
                pass
            return

        print()
        q_str = prompt_input("购买数量", default="1")
        try:
            quantity = int(q_str.strip()) if q_str.strip() else 1
            if quantity <= 0:
                quantity = 1
        except ValueError:
            quantity = 1

        self._items.append(ItemConfig(url=url.strip(), quantity=quantity))
        self._changed = True
        print(f"\n{C_GREEN}✓ 已添加商品: {url.strip()} x {quantity}{C_RESET}")
        try:
            sys.stdin.readline()
        except Exception:
            pass

    def _edit_item(self) -> None:
        if not self._items:
            return

        while True:
            clear_screen()
            show_cursor()
            print(f"\n{C_BRIGHT}── 选择要编辑的商品 ──{C_RESET}\n")

            for i, item in enumerate(self._items):
                print(f"  {i + 1}. {item.url[:60]}... x{item.quantity}" if len(item.url) > 60 else f"  {i + 1}. {item.url} x{item.quantity}")

            print(f"\n{C_DIM}输入序号编辑，Q返回{C_RESET}\n")
            try:
                line = sys.stdin.readline()
            except EOFError:
                break
            line = line.strip()
            if line.lower() in ("q", "quit", "exit"):
                break
            try:
                idx = int(line) - 1
                if 0 <= idx < len(self._items):
                    self._edit_single_item(idx)
                    break
                else:
                    print(f"{C_RED}序号超出范围{C_RESET}")
            except ValueError:
                pass

    def _edit_single_item(self, idx: int) -> None:
        clear_screen()
        show_cursor()
        item = self._items[idx]
        print(f"\n{C_BRIGHT}── 编辑商品 #{idx + 1} ──{C_RESET}\n")
        print(f"当前链接: {C_CYAN}{item.url}{C_RESET}")
        print(f"当前数量: {C_CYAN}{item.quantity}{C_RESET}\n")

        url = prompt_input("商品链接", default=item.url)
        if not url.strip():
            url = item.url
        print()
        q_str = prompt_input("购买数量", default=str(item.quantity))
        try:
            quantity = int(q_str.strip()) if q_str.strip() else item.quantity
            if quantity <= 0:
                quantity = item.quantity
        except ValueError:
            quantity = item.quantity

        self._items[idx] = ItemConfig(url=url.strip(), quantity=quantity)
        self._changed = True
        print(f"\n{C_GREEN}✓ 已更新商品{C_RESET}")
        try:
            sys.stdin.readline()
        except Exception:
            pass

    def _remove_item(self) -> None:
        if not self._items:
            return

        clear_screen()
        show_cursor()
        print(f"\n{C_BRIGHT}── 删除商品 ──{C_RESET}\n")

        for i, item in enumerate(self._items):
            print(f"  {i + 1}. {item.url[:60]}... x{item.quantity}" if len(item.url) > 60 else f"  {i + 1}. {item.url} x{item.quantity}")

        print(f"\n{C_DIM}输入要删除的序号，或 'A' 删除全部{C_RESET}\n")
        try:
            line = sys.stdin.readline()
        except EOFError:
            return
        line = line.strip()
        if line.lower() == "a":
            if confirm(f"确认删除全部 {len(self._items)} 个商品？", default=False):
                self._items.clear()
                self._changed = True
                print(f"{C_GREEN}✓ 已删除全部商品{C_RESET}")
        elif line.lower() in ("q", "quit", "exit", ""):
            return
        else:
            try:
                idx = int(line) - 1
                if 0 <= idx < len(self._items):
                    removed = self._items.pop(idx)
                    self._changed = True
                    print(f"{C_GREEN}✓ 已删除: {removed.url[:50]}...{C_RESET}")
                else:
                    print(f"{C_RED}序号超出范围{C_RESET}")
            except ValueError:
                print(f"{C_RED}无效输入{C_RESET}")

        try:
            sys.stdin.readline()
        except Exception:
            pass

    def _do_save(self) -> None:
        if self._save_config():
            print(f"\n{C_GREEN}✓ 配置文件已保存至: {self._config_path}{C_RESET}")
        else:
            print(f"\n{C_RED}✗ 保存失败{C_RESET}")
        try:
            sys.stdin.readline()
        except Exception:
            pass

    def _do_run(self, dry_run: bool) -> None:
        if not self._save_config():
            try:
                sys.stdin.readline()
            except Exception:
                pass
            return

        mode_str = "Dry-Run" if dry_run else "正式运行"
        if not confirm(f"确认开始 {mode_str}？", default=True):
            return

        show_cursor()
        clear_screen()

        from app import AppRuntimeError, PurchaseApp
        from status import ConsoleStatusSink

        sink = ConsoleStatusSink(stream=sys.stdout)
        try:
            config = load_config(self._config_path)
            purchase_time = None
            result = PurchaseApp().run(config, sink, dry_run=dry_run, purchase_time=purchase_time)
            print(f"\n{C_GREEN}✓ {result.message}{C_RESET}")
        except (ConfigValidationError, AppRuntimeError) as exc:
            print(f"\n{C_RED}✗ 运行失败: {exc}{C_RESET}")
        finally:
            sink.close()

        print(f"\n{C_DIM}按 Enter 返回配置界面...{C_RESET}")
        try:
            sys.stdin.readline()
        except Exception:
            pass


def run_interactive(config_path: Path) -> int:
    try:
        editor = InteractiveConfigEditor(config_path)
        editor.run()
        return 0
    except KeyboardInterrupt:
        show_cursor()
        clear_screen()
        return 0
    except Exception as exc:
        show_cursor()
        clear_screen()
        print(f"{C_RED}编辑器异常退出: {exc}{C_RESET}")
        return 1
