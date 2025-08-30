import functools
import datetime
import requests


@functools.cache
def get_prices(date: datetime.date, area="SE3"):
    return requests.get(
        "https://mgrey.se/espot", params={"format": "json", "date": date.isoformat()}
    ).json()[area]


def get_price(dt: datetime.datetime):
    prices = get_prices(dt.date())
    for p in prices:
        if p["hour"] == dt.hour:
            return p["price_sek"] * 0.01

    raise RuntimeError(f"failed to find hour {dt.hour}")
