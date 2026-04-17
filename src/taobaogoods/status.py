from __future__ import annotations

from dataclasses import dataclass
from getpass import getpass
from typing import Protocol
import sys


class StatusSink(Protocol):
    def set_status(self, message: str) -> None:
        ...

    def show_info(self, title: str, message: str) -> None:
        ...

    def show_error(self, title: str, message: str) -> None:
        ...

    def prompt_text(self, title: str, prompt: str, secret: bool = False) -> str | None:
        ...

    def close(self) -> None:
        ...


@dataclass
class ConsoleStatusSink:
    stream: object = sys.stdout

    def set_status(self, message: str) -> None:
        print(message, file=self.stream)

    def show_info(self, title: str, message: str) -> None:
        print(f"[{title}] {message}", file=self.stream)

    def show_error(self, title: str, message: str) -> None:
        print(f"[{title}] {message}", file=sys.stderr)

    def prompt_text(self, title: str, prompt: str, secret: bool = False) -> str | None:
        print(f"[{title}] {prompt}", file=self.stream)
        if secret:
            value = getpass("> ")
        else:
            value = input("> ")
        value = value.strip()
        return value or None

    def close(self) -> None:
        return None


class NullStatusSink(ConsoleStatusSink):
    def set_status(self, message: str) -> None:
        return None

    def show_info(self, title: str, message: str) -> None:
        return None

    def show_error(self, title: str, message: str) -> None:
        return None

    def prompt_text(self, title: str, prompt: str, secret: bool = False) -> str | None:
        return None
