from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog
except ImportError:  # pragma: no cover - tkinter may be unavailable in some runtimes.
    tk = None
    messagebox = None
    simpledialog = None


class TkStatusSink:
    def __init__(self, title: str = "TaoBaoGoods") -> None:
        if tk is None or messagebox is None or simpledialog is None:
            raise RuntimeError("tkinter is not available.")

        self._root = tk.Tk()
        self._root.title(title)
        self._root.geometry("500x220")
        self._root.resizable(False, False)

        self._status_label = tk.Label(
            self._root,
            text="初始化中...",
            font=("Microsoft YaHei UI", 12),
            justify="left",
            wraplength=440,
        )
        self._status_label.pack(padx=24, pady=36, fill="both", expand=True)
        self._pump()

    def set_status(self, message: str) -> None:
        self._status_label.config(text=message)
        self._pump()

    def show_info(self, title: str, message: str) -> None:
        messagebox.showinfo(title, message, parent=self._root)
        self._pump()

    def show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title, message, parent=self._root)
        self._pump()

    def prompt_text(self, title: str, prompt: str, secret: bool = False) -> str | None:
        value = simpledialog.askstring(
            title=title,
            prompt=prompt,
            parent=self._root,
            show="*" if secret else None,
        )
        if value is None:
            return None
        value = value.strip()
        return value or None

    def close(self) -> None:
        if self._root and self._root.winfo_exists():
            self._root.destroy()

    def _pump(self) -> None:
        self._root.update_idletasks()
        self._root.update()
