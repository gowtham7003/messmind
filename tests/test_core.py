from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from messmind.analytics import summarize
from messmind.demo import demo_records
from messmind.models import MealRecord
from messmind.storage import DuplicateMealError, MealStore


def meal(**overrides):
    data = dict(log_date="2026-01-01", meal="Lunch", menu="Rice and dal",
                prepared=100, served=80, unserved=0, cost_per_portion=25.0)
    data.update(overrides)
    return MealRecord(**data)


class MetricsTests(unittest.TestCase):
    def test_weighted_surplus_not_average_of_meal_percentages(self):
        result = summarize([meal(), meal(log_date="2026-01-02", prepared=10, served=5)])
        self.assertEqual((result.prepared, result.served, result.surplus), (110, 85, 25))
        self.assertAlmostEqual(result.surplus_rate, 100 * 25 / 110)
        self.assertEqual(result.surplus_value, 625.0)

    def test_shortage_is_included_in_demand(self):
        result = summarize([meal(prepared=80, served=80, unserved=20)])
        self.assertEqual(result.surplus_rate, 0)
        self.assertEqual(result.service_rate, 80)
        self.assertEqual(result.unserved, 20)

    def test_empty_or_zero_denominators_are_unknown_not_perfect(self):
        for records in ([], [meal(prepared=0, served=0)]):
            with self.subTest(records=records):
                result = summarize(records)
                self.assertIsNone(result.surplus_rate)
                self.assertIsNone(result.service_rate)
                self.assertEqual(result.surplus_value, 0)

    def test_entirely_unserved_service(self):
        result = summarize([meal(prepared=0, served=0, unserved=30)])
        self.assertEqual(result.service_rate, 0)
        self.assertIsNone(result.surplus_rate)

    def test_decimal_money_aggregation(self):
        result = summarize([meal(prepared=3, served=0, cost_per_portion=0.1)])
        self.assertEqual(result.surplus_value, 0.3)


class ValidationTests(unittest.TestCase):
    def test_rejects_impossible_or_nonfinite_values(self):
        cases = [dict(served=101), dict(prepared=-1), dict(unserved=-1),
                 dict(prepared=1.5), dict(prepared=True), dict(unserved=5),
                 dict(menu="   "), dict(meal="Snack"), dict(log_date="2026-02-30"),
                 dict(log_date="20260101"), dict(cost_per_portion=float("nan")),
                 dict(cost_per_portion=float("inf")), dict(cost_per_portion=-1),
                 dict(prepared=100001), dict(menu="a" * 121),
                 dict(log_date=(date.today() + timedelta(days=1)).isoformat()),
                 dict(prepared=100000, served=100000, unserved=1)]
        for overrides in cases:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                meal(**overrides)


class StorageTests(unittest.TestCase):
    def test_persists_across_reopen_and_does_not_overwrite_duplicate(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "meals.db"
            store = MealStore(path)
            original = meal(menu="Chef's lunch; SELECT 1;")
            store.add(original)
            with self.assertRaises(DuplicateMealError):
                store.add(meal(served=90))
            self.assertEqual(MealStore(path).list_all(), [original])

    def test_same_day_different_meals_and_order(self):
        with TemporaryDirectory() as tmp:
            store = MealStore(Path(tmp) / "meals.db")
            for service in ("Dinner", "Breakfast", "Lunch"):
                store.add(meal(meal=service))
            self.assertEqual([r.meal for r in store.list_all()], ["Breakfast", "Lunch", "Dinner"])


class DemoTests(unittest.TestCase):
    def test_demo_is_reproducible_and_has_valid_surplus_and_shortage(self):
        end = date(2026, 1, 28)
        records = demo_records(end)
        self.assertEqual(records, demo_records(end))
        self.assertEqual(len(records), 84)
        self.assertEqual(len({(r.log_date, r.meal) for r in records}), 84)
        self.assertTrue(any(r.unserved for r in records))
        self.assertTrue(any(r.surplus for r in records))


if __name__ == "__main__":
    unittest.main()
