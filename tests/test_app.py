from pathlib import Path
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from app import AppRuntimeError, PurchaseApp
from config import AppConfig, ItemConfig


class FakeStatusSink:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def set_status(self, message: str) -> None:
        self.messages.append(message)

    def show_info(self, title: str, message: str) -> None:
        self.messages.append(f"{title}:{message}")

    def show_error(self, title: str, message: str) -> None:
        self.messages.append(f"{title}:{message}")

    def prompt_text(self, title: str, prompt: str, secret: bool = False) -> str | None:
        return None

    def close(self) -> None:
        return None


class FakeSession:
    def __init__(self, should_fail: bool = False) -> None:
        self.events: list[str] = []
        self.closed = 0
        self.should_fail = should_fail

    def login(self, username: str, password: str) -> None:
        self.events.append(f"login:{username}:{password}")

    def add_to_cart(self, url: str, quantity: int) -> None:
        self.events.append(f"add:{url}:{quantity}")
        if self.should_fail:
            raise RuntimeError("broken add_to_cart")

    def checkout(self) -> None:
        self.events.append("checkout")

    def place_order(self) -> None:
        self.events.append("place_order")

    def capture_debug_artifact(self, action: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / f"{action}.png"
            path.write_text("", encoding="utf-8")
            return path

    def close(self) -> None:
        self.closed += 1


class AppTests(unittest.TestCase):
    def setUp(self) -> None:
        driver_file = PROJECT_ROOT / "tests" / "fake-driver.exe"
        driver_file.write_text("", encoding="utf-8")
        self.addCleanup(driver_file.unlink)
        self.config = AppConfig(
            window_size="1280,720",
            proxy="",
            driver_path=str(driver_file),
            username="user",
            password="password",
            items=(ItemConfig(url="https://example.com/item1", quantity=1),),
        )

    def test_run_executes_expected_order(self) -> None:
        session = FakeSession()
        app = PurchaseApp(session_factory=lambda _config: session)

        result = app.run(self.config, FakeStatusSink())

        self.assertTrue(result.success)
        self.assertEqual(
            session.events,
            [
                "login:user:password",
                "add:https://example.com/item1:1",
                "checkout",
                "place_order",
            ],
        )
        self.assertEqual(session.closed, 1)

    def test_run_closes_session_on_failure(self) -> None:
        session = FakeSession(should_fail=True)
        app = PurchaseApp(session_factory=lambda _config: session)

        with self.assertRaises(AppRuntimeError):
            app.run(self.config, FakeStatusSink())

        self.assertEqual(session.closed, 1)

    def test_dry_run_skips_session_creation(self) -> None:
        app = PurchaseApp(session_factory=lambda _config: self.fail("session should not be created"))

        result = app.run(self.config, FakeStatusSink(), dry_run=True)

        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main()
