"""Meal records and validation shared by the UI and database."""

from dataclasses import dataclass
from datetime import date
from math import isfinite

MEALS = ("Breakfast", "Lunch", "Dinner")
MAX_PORTIONS = 100_000


@dataclass(frozen=True)
class MealRecord:
    log_date: str
    meal: str
    menu: str
    prepared: int
    served: int
    unserved: int = 0
    cost_per_portion: float = 0.0

    def __post_init__(self):
        try:
            parsed = date.fromisoformat(self.log_date)
        except (TypeError, ValueError):
            raise ValueError("Use a valid date in YYYY-MM-DD format.") from None
        if parsed.isoformat() != self.log_date:
            raise ValueError("Use a date in YYYY-MM-DD format.")
        if parsed > date.today():
            raise ValueError("Meal logs must be for today or an earlier date.")
        if self.meal not in MEALS:
            raise ValueError("Choose Breakfast, Lunch, or Dinner.")
        if not isinstance(self.menu, str) or not 1 <= len(self.menu.strip()) <= 120:
            raise ValueError("Enter a menu description of 1 to 120 characters.")
        object.__setattr__(self, "menu", self.menu.strip())
        for label in ("prepared", "served", "unserved"):
            value = getattr(self, label)
            if type(value) is not int or not 0 <= value <= MAX_PORTIONS:
                raise ValueError(f"{label.capitalize()} must be a whole number from 0 to {MAX_PORTIONS:,}.")
        if self.served > self.prepared:
            raise ValueError("Meals served cannot exceed meals prepared.")
        if self.unserved and self.served < self.prepared:
            raise ValueError("For one meal type, unserved requests and unused portions cannot both be positive.")
        if self.demand > MAX_PORTIONS:
            raise ValueError(f"Total demand cannot exceed {MAX_PORTIONS:,} portions.")
        if (type(self.cost_per_portion) not in (int, float)
                or not isfinite(self.cost_per_portion)
                or not 0 <= self.cost_per_portion <= 10_000):
            raise ValueError("Cost per portion must be between ₹0 and ₹10,000.")

    @property
    def surplus(self):
        return self.prepared - self.served

    @property
    def demand(self):
        """Includes recorded requests that could not be served."""
        return self.served + self.unserved
