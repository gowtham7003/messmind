"""Transparent metrics; no trained prediction model in Day 1."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

from .models import MealRecord


@dataclass(frozen=True)
class Summary:
    meal_count: int
    prepared: int
    served: int
    surplus: int
    unserved: int
    surplus_rate: float | None
    service_rate: float | None
    surplus_value: float


def summarize(records: Iterable[MealRecord]) -> Summary:
    records = list(records)
    prepared = sum(r.prepared for r in records)
    served = sum(r.served for r in records)
    surplus = prepared - served
    unserved = sum(r.unserved for r in records)
    demand = served + unserved
    value = sum((Decimal(str(r.cost_per_portion)) * r.surplus for r in records), Decimal(0))
    return Summary(
        meal_count=len(records), prepared=prepared, served=served,
        surplus=surplus, unserved=unserved,
        surplus_rate=100 * surplus / prepared if prepared else None,
        service_rate=100 * served / demand if demand else None,
        surplus_value=float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
    )
