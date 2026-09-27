"""End-to-end Streamlit state checks, using a temporary database."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class AppFlowTests(unittest.TestCase):
    def test_demo_save_duplicate_invalid_and_return_to_demo(self):
        with TemporaryDirectory() as tmp:
            db = Path(tmp) / "ledger.db"
            with patch.dict("os.environ", {"MESSMIND_DB_PATH": str(db)}):
                app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()
                self.assertFalse(app.exception)
                self.assertFalse(db.exists(), "Demo mode must not create a real ledger")
                self.assertTrue(any("synthetic" in item.value for item in app.info))
                app.radio(key="source").set_value("My kitchen").run()
                self.assertFalse(app.exception)
                app.text_input(key="menu").set_value("Rice and vegetables")
                app.button[0].click().run()
                self.assertFalse(app.exception)
                self.assertTrue(any("Meal saved" in item.value for item in app.success))
                self.assertEqual(app.metric[0].value, "200")
                self.assertEqual(app.metric[2].value, "20")
                app.button[0].click().run()
                self.assertTrue(any("already recorded" in item.value for item in app.error))
                self.assertEqual(app.metric[0].value, "200")
                app.number_input(key="served").set_value(201)
                app.button[0].click().run()
                self.assertTrue(any("cannot exceed" in item.value for item in app.error))
                app.radio(key="source").set_value("Demo kitchen").run()
                self.assertFalse(app.exception)
                self.assertNotEqual(app.metric[0].value, "200")
                app.radio(key="source").set_value("My kitchen").run()
                self.assertEqual(app.metric[0].value, "200")


if __name__ == "__main__":
    unittest.main()
