from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from paths import ARTIFACTS_DIR, CONFIG_DIR, DEFAULT_CONFIG_PATH, PROJECT_ROOT as PACKAGE_PROJECT_ROOT


class PathTests(unittest.TestCase):
    def test_package_project_root_matches_python_version_directory(self) -> None:
        self.assertEqual(PACKAGE_PROJECT_ROOT, PROJECT_ROOT)

    def test_default_config_path_points_to_config_directory(self) -> None:
        self.assertEqual(DEFAULT_CONFIG_PATH, CONFIG_DIR / "default.yaml")
        self.assertEqual(DEFAULT_CONFIG_PATH.name, "default.yaml")

    def test_artifacts_directory_stays_inside_project_root(self) -> None:
        self.assertEqual(ARTIFACTS_DIR.parent, PROJECT_ROOT)


if __name__ == "__main__":
    unittest.main()
