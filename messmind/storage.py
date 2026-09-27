"""A local SQLite ledger. Demo records never enter this database."""

from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
import sqlite3

from .models import MealRecord


class DuplicateMealError(ValueError):
    pass


class MealStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS meals (
                    log_date TEXT NOT NULL,
                    meal TEXT NOT NULL CHECK(meal IN ('Breakfast', 'Lunch', 'Dinner')),
                    menu TEXT NOT NULL,
                    prepared INTEGER NOT NULL CHECK(prepared >= 0),
                    served INTEGER NOT NULL CHECK(served >= 0 AND served <= prepared),
                    unserved INTEGER NOT NULL CHECK(unserved >= 0),
                    cost_per_portion REAL NOT NULL CHECK(cost_per_portion >= 0),
                    PRIMARY KEY(log_date, meal),
                    CHECK(unserved = 0 OR served = prepared)
                )
            """)

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def add(self, record: MealRecord):
        with self.connect() as conn:
            try:
                conn.execute("""
                    INSERT INTO meals
                    (log_date, meal, menu, prepared, served, unserved, cost_per_portion)
                    VALUES (:log_date, :meal, :menu, :prepared, :served, :unserved, :cost_per_portion)
                """, asdict(record))
            except sqlite3.IntegrityError as exc:
                if "UNIQUE constraint failed" in str(exc):
                    raise DuplicateMealError(
                        f"{record.meal} on {record.log_date} is already recorded. No data was replaced."
                    ) from None
                raise

    def list_all(self) -> list[MealRecord]:
        with self.connect() as conn:
            rows = conn.execute("""
                SELECT log_date, meal, menu, prepared, served, unserved, cost_per_portion
                FROM meals ORDER BY log_date DESC,
                CASE meal WHEN 'Breakfast' THEN 1 WHEN 'Lunch' THEN 2 ELSE 3 END
            """).fetchall()
        return [MealRecord(**dict(row)) for row in rows]
