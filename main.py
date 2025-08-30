import fire
import datetime
from typing import Tuple
import zaptec
import requests_cache
import mgrey

# Install a filesystem cache
requests_cache.install_cache(
    ".http_cache",  # folder name for cached files
    backend="filesystem",  # use filesystem backend
    expire_after=3600,  # cache expiration in seconds (1 hour)
)


def parse_quarter(quarter: str) -> Tuple[datetime.datetime, datetime.datetime]:
    current_year = datetime.datetime.now().year
    local_tz = datetime.datetime.now().astimezone().tzinfo

    if quarter.upper() == "Q1":
        year = current_year
        start_date = datetime.datetime(year, 1, 1, tzinfo=local_tz)
        end_date = datetime.datetime(year, 3, 31, 23, 59, 59, tzinfo=local_tz)
    elif quarter.upper() == "Q2":
        year = current_year
        start_date = datetime.datetime(year, 4, 1, tzinfo=local_tz)
        end_date = datetime.datetime(year, 6, 30, 23, 59, 59, tzinfo=local_tz)
    elif quarter.upper() == "Q3":
        year = current_year
        start_date = datetime.datetime(year, 7, 1, tzinfo=local_tz)
        end_date = datetime.datetime(year, 9, 30, 23, 59, 59, tzinfo=local_tz)
    elif quarter.upper() == "Q4":
        year = current_year - 1  # Previous year for Q4
        start_date = datetime.datetime(year, 10, 1, tzinfo=local_tz)
        end_date = datetime.datetime(year, 12, 31, 23, 59, 59, tzinfo=local_tz)
    else:
        raise ValueError(f"Invalid quarter: {quarter}. Must be Q1, Q2, Q3, or Q4")

    return start_date, end_date


def main(quarter: str = "Q2", charger="all"):
    show_charger = charger
    try:
        start_date, end_date = parse_quarter(quarter)

        chargers = zaptec.list_chargers()

        for charger in chargers:
            if show_charger != "all" and show_charger != charger.get("Name", "Unknown"):
                continue

            energy_details, charges_count = zaptec.get_energy_history(
                charger.get("Id"), start_date, end_date, page_size=50
            )
            total_cost = 0.0
            total_energy = 0.0
            for energy_detail in energy_details:
                if energy_detail["Energy"] == 0:
                    continue
                dt = datetime.datetime.fromisoformat(energy_detail["Timestamp"])
                # charged energy is reported every 15 minutes how much was charged before, but we need the price from previous
                dt = dt - datetime.timedelta(minutes=1)
                price = mgrey.get_price(dt)
                energy_detail["Price"] = price
                cost = energy_detail["Energy"] * price
                total_energy += energy_detail["Energy"]
                energy_detail["Cost"] = cost
                total_cost += cost                

            print(f"Name: {charger.get('Name', 'Unknown')}")
            # print(f"Serial: {charger.get('SerialNo', 'Unknown')}")
            # print(f"Device ID: {charger.get('DeviceId', 'Unknown')}")
            # print(f"Connection: {online}")
            # print(f"Operating Mode: {mode}")
            # print(f"Installation: {charger.get('InstallationName', 'Unknown')}")
            print(f"Charges: {charges_count}")
            print(f"Total energy: {total_energy}")
            print(f"Total cost: {total_cost}")
            print("-" * 40)
            # break

    except Exception as e:
        print(f"Error fetching chargers: {e}")


if __name__ == "__main__":
    fire.Fire(main)
