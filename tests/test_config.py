from pathlib import Path
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from config import ConfigValidationError, load_config, resolve_credentials, validate_runtime_prerequisites


class ConfigTests(unittest.TestCase):
    def test_missing_config_creates_default_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config" / "default.yaml"
            config = load_config(config_path)

            self.assertTrue(config_path.exists())
            self.assertEqual(config.window_size, "1280,720")
            self.assertEqual(len(config.items), 1)

    def test_environment_credentials_override_file_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config_path.write_text(
                """
window_size: "1280,720"
proxy: ""
driver_path: "chromedriver.exe"
username: "file_user"
password: "file_password"
items:
  - url: "https://example.com/item1"
    quantity: 1
""".strip(),
                encoding="utf-8",
            )

            config = load_config(config_path, env={})
            credentials = resolve_credentials(
                config,
                env={
                    "TAOBAOGOODS_USERNAME": "env_user",
                    "TAOBAOGOODS_PASSWORD": "env_password",
                },
            )

            self.assertIsNotNone(credentials)
            self.assertEqual(credentials.username, "env_user")
            self.assertEqual(credentials.password, "env_password")

    def test_invalid_quantity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config_path.write_text(
                """
window_size: "1280,720"
proxy: ""
driver_path: "chromedriver.exe"
items:
  - url: "https://example.com/item1"
    quantity: 0
""".strip(),
                encoding="utf-8",
            )

            with self.assertRaises(ConfigValidationError):
                load_config(config_path)

    def test_runtime_validation_accepts_existing_driver_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            driver_path = Path(temp_dir) / "chromedriver.exe"
            driver_path.write_text("", encoding="utf-8")
            config_path = Path(temp_dir) / "config.yaml"
            driver_path_str = str(driver_path).replace("\\", "\\\\")
            config_path.write_text(
                rf"""
window_size: "1280,720"
proxy: ""
driver_path: "{driver_path_str}"
items:
  - url: "https://example.com/item1"
    quantity: 1
""".strip(),
                encoding="utf-8",
            )

            config = load_config(config_path)
            validate_runtime_prerequisites(config)


if __name__ == "__main__":
    unittest.main()
