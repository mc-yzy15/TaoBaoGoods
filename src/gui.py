from __future__ import annotations

import threading
from pathlib import Path

import flet as ft

from src.app import AppRuntimeError, PurchaseApp
from src.config import AppConfig, ItemConfig, load_config


class FletStatusSink:
    """StatusSink that updates Flet UI controls from a background thread."""

    def __init__(
        self,
        status_text: ft.Text,
        log_view: ft.Column,
        progress_bar: ft.ProgressBar,
        page: ft.Page,
    ) -> None:
        self._status = status_text
        self._log = log_view
        self._progress = progress_bar
        self._page = page
        self._step_index = 0
        self._total_steps = 5  # login, add_to_cart x N, checkout, place_order
        self._step_index = 0

    def set_status(self, message: str) -> None:
        self._status.value = message
        self._step_index += 1
        self._progress.value = min(self._step_index / self._total_steps, 0.95)
        self._log.controls.append(
            ft.Text(f"[{self._step_index}] {message}", size=12, color=ft.Colors.GREY_700)
        )
        self._page.update()

    def show_info(self, title: str, message: str) -> None:
        self._log.controls.append(
            ft.Text(f"[{title}] {message}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
        )
        self._page.update()

    def show_error(self, title: str, message: str) -> None:
        self._log.controls.append(
            ft.Text(f"[{title}] 错误: {message}", size=12, color=ft.Colors.RED_700)
        )
        self._page.update()

    def prompt_text(self, title: str, prompt: str, secret: bool = False) -> str | None:
        return None  # Flet 模式下从配置页填，不走运行时弹窗

    def close(self) -> None:
        self._progress.value = 1.0
        self._page.update()


class FletGUI:
    """Flet-based GUI for TaoBaoGoods."""

    APP_NAME = "TaoBaoGoods - 淘宝自动购"
    COLORS = {
        "card_bg": ft.Colors.SURFACE_CONTAINER_HIGHEST,
        "accent": ft.Colors.BLUE_700,
        "success": ft.Colors.GREEN_700,
        "error": ft.Colors.RED_700,
    }

    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path
        self._load_config_data()

        # Flet controls — assigned during build()
        self._page: ft.Page | None = None
        self._body_container: ft.Container | None = None

        # Config page controls
        self._tf_window_size: ft.TextField | None = None
        self._tf_proxy: ft.TextField | None = None
        self._tf_driver_path: ft.TextField | None = None
        self._tf_username: ft.TextField | None = None
        self._tf_password: ft.TextField | None = None
        self._item_list_column: ft.Column | None = None
        self._item_count_text: ft.Text | None = None

        # Run page controls
        self._status_text: ft.Text | None = None
        self._progress_bar: ft.ProgressBar | None = None
        self._log_view: ft.Column | None = None

        # Threading
        self._cancel_event = threading.Event()
        self._run_thread: threading.Thread | None = None

        # File picker
        self._file_picker: ft.FilePicker | None = None

    # ── Config data helpers ──────────────────────────────────────────

    def _load_config_data(self) -> None:
        try:
            config = load_config(self._config_path)
            self._window_size = config.window_size
            self._proxy = config.proxy
            self._driver_path = config.driver_path
            self._username = config.username or ""
            self._password = config.password or ""
            self._items: list[ItemConfig] = list(config.items)
        except Exception:
            self._window_size = "1280,720"
            self._proxy = ""
            self._driver_path = "chromedriver.exe"
            self._username = ""
            self._password = ""
            self._items = []

    def _collect_form_config(self) -> AppConfig:
        return AppConfig(
            window_size=self._tf_window_size.value.strip() or "1280,720",
            proxy=self._tf_proxy.value.strip(),
            driver_path=self._tf_driver_path.value.strip() or "chromedriver.exe",
            username=self._tf_username.value.strip() or None,
            password=self._tf_password.value.strip() or None,
            items=tuple(self._items),
        )

    def _save_config(self) -> bool:
        if not self._tf_driver_path.value.strip():
            self._page.snack_bar = ft.SnackBar(
                ft.Text("ChromeDriver 路径不能为空"), bgcolor=ft.Colors.RED_700
            )
            self._page.snack_bar.open = True
            self._page.update()
            return False

        parts = self._tf_window_size.value.strip().split(",")
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            self._page.snack_bar = ft.SnackBar(
                ft.Text("窗口大小格式无效，请使用 宽,高 格式，如 1280,720"),
                bgcolor=ft.Colors.RED_700,
            )
            self._page.snack_bar.open = True
            self._page.update()
            return False

        item_lines: list[str] = []
        for item in self._items:
            item_lines.append(f"  - url: \"{item.url}\"")
            item_lines.append(f"    quantity: {item.quantity}")
        items_text = "\n".join(item_lines) if item_lines else "  - url: \"\"\n    quantity: 1"

        config_text = (
            f"# TaoBaoGoods configuration\n"
            f"window_size: \"{self._tf_window_size.value.strip()}\"\n"
            f"proxy: \"{self._tf_proxy.value.strip()}\"\n"
            f"driver_path: \"{self._tf_driver_path.value.strip()}\"\n"
            f"username: \"{self._tf_username.value.strip()}\"\n"
            f"password: \"{self._tf_password.value.strip()}\"\n"
            f"items:\n{items_text}\n"
        )
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            self._config_path.write_text(config_text, encoding="utf-8")
            return True
        except Exception as e:
            self._page.snack_bar = ft.SnackBar(
                ft.Text(f"保存失败: {e}"), bgcolor=ft.Colors.RED_700
            )
            self._page.snack_bar.open = True
            self._page.update()
            return False

    # ── Build: entry point called by ft.app(target=...) ──────────────

    def build(self, page: ft.Page) -> None:
        self._page = page
        page.title = self.APP_NAME
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.window.width = 820
        page.window.height = 720
        page.window.min_width = 640
        page.window.min_height = 500
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 0

        # File picker for ChromeDriver
        self._file_picker = ft.FilePicker(on_result=self._on_file_picked)
        page.overlay.append(self._file_picker)

        self._body_container = ft.Container(expand=True, padding=20)
        page.add(self._body_container)
        self._build_config_page()

    def _on_file_picked(self, e: ft.FilePickerResultEvent) -> None:
        if e.files and len(e.files) > 0 and self._tf_driver_path is not None:
            self._tf_driver_path.value = e.files[0].path
            self._tf_driver_path.update()

    # ── Config Page ─────────────────────────────────────────────────

    def _build_config_page(self) -> None:
        """Rebuild the config editor page."""
        self._cancel_event.clear()

        # -- Form fields --
        self._tf_window_size = ft.TextField(
            label="窗口大小", value=self._window_size,
            hint_text="宽,高 例如 1280,720", width=260,
        )
        self._tf_proxy = ft.TextField(
            label="代理服务器", value=self._proxy,
            hint_text="http://127.0.0.1:7890", width=400,
        )
        self._tf_driver_path = ft.TextField(
            label="ChromeDriver 路径", value=self._driver_path,
            hint_text="chromedriver.exe 或绝对路径", expand=True,
        )
        self._tf_username = ft.TextField(
            label="用户名", value=self._username, width=320,
        )
        self._tf_password = ft.TextField(
            label="密码", value=self._password,
            password=True, can_reveal_password=True, width=320,
        )

        # -- Item list --
        self._item_count_text = ft.Text(f"{len(self._items)} 个商品", size=14)
        self._item_list_column = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)
        self._refresh_item_list()

        # -- Page body --
        page = self._page
        body = ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SHOPPING_CART_CHECKOUT, size=32, color=self.COLORS["accent"]),
                            ft.Text(self.APP_NAME, size=26, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.Text("v1.2", size=12, color=ft.Colors.GREY_500),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    margin=ft.margin.only(bottom=16),
                ),

                # Basic settings card
                self._card("📋 基础设置", [
                    self._tf_window_size,
                    self._tf_proxy,
                    ft.Row([self._tf_driver_path, self._build_pick_driver_btn()], spacing=8),
                ]),

                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),

                # Credentials card
                self._card("🔐 登录凭据", [
                    ft.Row([self._tf_username, self._tf_password], spacing=16),
                ]),

                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),

                # Items card
                self._card("📦 商品列表", [
                    ft.Row(
                        controls=[
                            self._item_count_text,
                            ft.Container(expand=True),
                            ft.FilledButton("+ 添加商品", icon=ft.Icons.ADD,
                                            on_click=self._on_add_item),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        content=self._item_list_column,
                        height=200,
                        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                        border_radius=8,
                        padding=8,
                    ),
                ]),

                ft.Divider(height=16, color=ft.Colors.TRANSPARENT),

                # Action buttons
                ft.Row(
                    controls=[
                        ft.OutlinedButton("💾 保存配置", icon=ft.Icons.SAVE,
                                          on_click=self._on_save),
                        ft.OutlinedButton("🔍 Dry-Run", icon=ft.Icons.SEARCH,
                                          on_click=lambda e: self._on_run(dry_run=True)),
                        ft.Container(expand=True),
                        ft.FilledTonalButton("▶ 开始运行", icon=ft.Icons.PLAY_ARROW,
                                              on_click=lambda e: self._on_run(dry_run=False)),
                    ],
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

        self._body_container.content = body
        page.update()

    def _build_pick_driver_btn(self) -> ft.IconButton:
        return ft.IconButton(
            icon=ft.Icons.FOLDER_OPEN, tooltip="浏览",
            on_click=lambda e: self._file_picker.pick_files(
                dialog_title="选择 ChromeDriver",
                file_type=ft.FilePickerFileType.ANY,
                allow_multiple=False,
            ),
        )

    # ── Item management ─────────────────────────────────────────────

    def _refresh_item_list(self) -> None:
        col = self._item_list_column
        col.controls.clear()
        if not self._items:
            col.controls.append(
                ft.Text("暂无商品，点击右上角「添加商品」", color=ft.Colors.GREY_400, italic=True)
            )
            return
        for idx, item in enumerate(self._items):
            url_short = item.url[:55] + "..." if len(item.url) > 55 else item.url
            row = ft.Row(
                controls=[
                    ft.Text(f"{idx+1}.", size=13, color=ft.Colors.GREY_600),
                    ft.Text(url_short, size=13, expand=True),
                    ft.Container(width=8),
                    ft.Text(f"x{item.quantity}", size=13, weight=ft.FontWeight.BOLD),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE, icon_size=18,
                        icon_color=ft.Colors.RED_400,
                        tooltip="删除",
                        on_click=lambda e, i=idx: self._on_delete_item(i),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            col.controls.append(
                ft.Container(
                    content=row,
                    padding=ft.padding.symmetric(vertical=2, horizontal=4),
                    border_radius=6,
                )
            )
        if self._item_count_text is not None:
            self._item_count_text.value = f"{len(self._items)} 个商品"

    def _on_add_item(self, e) -> None:
        url_field = ft.TextField(label="商品链接", hint_text="https://item.taobao.com/...", expand=True)
        qty_field = ft.TextField(label="数量", value="1", width=80, text_align=ft.TextAlign.RIGHT,
                                  keyboard_type=ft.KeyboardType.NUMBER)
        dlg = ft.AlertDialog(
            title=ft.Text("添加商品"),
            content=ft.Column([url_field, qty_field], tight=True, width=400),
            actions=[
                ft.TextButton("取消", on_click=lambda e: self._close_dialog(dlg)),
                ft.FilledButton("添加", on_click=lambda e: self._confirm_add_item(dlg, url_field, qty_field)),
            ],
        )
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def _confirm_add_item(self, dlg: ft.AlertDialog, url_field: ft.TextField,
                          qty_field: ft.TextField) -> None:
        url = url_field.value.strip()
        if not url:
            return
        try:
            qty = max(1, int(qty_field.value.strip() or "1"))
        except ValueError:
            qty = 1
        self._items.append(ItemConfig(url=url, quantity=qty))
        self._close_dialog(dlg)
        self._refresh_item_list()
        self._page.update()

    def _on_delete_item(self, idx: int) -> None:
        if 0 <= idx < len(self._items):
            self._items.pop(idx)
            self._refresh_item_list()
            self._page.update()

    def _close_dialog(self, dlg: ft.AlertDialog) -> None:
        dlg.open = False
        self._page.update()

    # ── Run Page ────────────────────────────────────────────────────

    def _build_run_page(self) -> None:
        """Switch to the run-status page."""
        self._status_text = ft.Text("准备就绪", size=20, weight=ft.FontWeight.BOLD)
        self._progress_bar = ft.ProgressBar(value=0, width=None, color=self.COLORS["accent"])
        self._log_view = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO)

        body = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ROCKET_LAUNCH, size=28, color=self.COLORS["accent"]),
                        ft.Text("运行状态", size=22, weight=ft.FontWeight.BOLD),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            self._status_text,
                            ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                            self._progress_bar,
                        ]),
                        padding=20,
                    )
                ),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                ft.Text("日志", size=14, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=self._log_view,
                            padding=8,
                        ),
                    ]),
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=8,
                    expand=True,
                ),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    controls=[
                        ft.OutlinedButton("◀ 返回配置", icon=ft.Icons.ARROW_BACK,
                                          on_click=self._on_back_to_config),
                        ft.Container(expand=True),
                        ft.FilledTonalButton("⏹ 取消运行", icon=ft.Icons.STOP,
                                              on_click=self._on_cancel_run),
                    ],
                ),
            ],
            spacing=0,
            expand=True,
        )

        self._body_container.content = body
        self._page.update()

    # ── Event handlers ──────────────────────────────────────────────

    def _on_save(self, e) -> None:
        if self._save_config():
            self._page.snack_bar = ft.SnackBar(
                ft.Text("✅ 配置已保存"), bgcolor=ft.Colors.GREEN_700
            )
        self._page.snack_bar.open = True
        self._page.update()

    def _on_run(self, dry_run: bool = False) -> None:
        if not self._save_config():
            return
        self._build_run_page()
        self._status_text.value = "Dry-Run 模式" if dry_run else "正在启动..."
        self._page.update()

        self._cancel_event.clear()
        self._run_thread = threading.Thread(
            target=self._run_purchase,
            args=(dry_run,),
            daemon=True,
        )
        self._run_thread.start()

    def _run_purchase(self, dry_run: bool) -> None:
        sink = FletStatusSink(
            status_text=self._status_text,
            log_view=self._log_view,
            progress_bar=self._progress_bar,
            page=self._page,
        )
        try:
            config = load_config(self._config_path)
            result = PurchaseApp().run(
                config, sink,
                dry_run=dry_run,
                purchase_time=None,
            )
            sink.show_info("完成", result.message)
        except (AppRuntimeError, Exception) as exc:
            sink.show_error("运行失败", str(exc))
        finally:
            sink.close()

    def _on_cancel_run(self, e) -> None:
        self._cancel_event.set()
        self._page.snack_bar = ft.SnackBar(ft.Text("⏹ 正在取消..."))
        self._page.snack_bar.open = True
        self._page.update()

    def _on_back_to_config(self, e) -> None:
        self._load_config_data()
        self._build_config_page()

    # ── Helpers ─────────────────────────────────────────────────────

    def _card(self, title: str, controls: list[ft.Control]) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                        *controls,
                    ],
                    spacing=10,
                ),
                padding=16,
            ),
        )
