"""Reproducible synthetic data, never presented as real kitchen results."""

from datetime import date, timedelta
from random import Random

from .models import MEALS, MealRecord

MENUS = {
    "Breakfast": ("Idli and sambar", "Dosa and chutney", "Pongal", "Upma"),
    "Lunch": ("Rice and sambar", "Vegetable biryani", "Lemon rice", "Chapati and dal"),
    "Dinner": ("Chapati and kurma", "Dosa", "Rice and rasam", "Vegetable pulao"),
}


def demo_records(end_date: date | None = None) -> list[MealRecord]:
    end_date = end_date or date.today() - timedelta(days=1)
    rng = Random(41)
    records = []
    for offset in range(28):
        day = end_date - timedelta(days=27 - offset)
        weekend = day.weekday() >= 5
        for meal in MEALS:
            center = {"Breakfast": 155, "Lunch": 215, "Dinner": 180}[meal]
            demand = center - (35 if weekend else 0) + rng.randint(-22, 22)
            prepared = center + rng.randint(-10, 20)
            served = min(prepared, demand)
            records.append(MealRecord(
                log_date=day.isoformat(), meal=meal,
                menu=MENUS[meal][offset % len(MENUS[meal])],
                prepared=prepared, served=served, unserved=max(0, demand - served),
                cost_per_portion={"Breakfast": 22.0, "Lunch": 40.0, "Dinner": 32.0}[meal],
            ))
    return records
