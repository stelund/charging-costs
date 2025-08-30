import fire
import datetime
from typing import Tuple
import zaptec
import requests_cache
import mgrey
import config
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.status import Status

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
    # Check credentials early, before initializing Rich console
    try:
        config.get_zaptec_credentials()
    except Exception as e:
        print(f"Error with credentials: {e}")
        return

    console = Console()
    show_charger = charger

    try:
        start_date, end_date = parse_quarter(quarter)
        console.print(
            f"Querying for {quarter} for [bold]{start_date.date().isoformat()}[/bold] - [bold]{end_date.date().isoformat()}[/bold]\n"
        )

        with Status("Fetching chargers list...", console=console):
            chargers = zaptec.list_chargers()

        filtered_chargers = [
            c
            for c in chargers
            if show_charger == "all" or show_charger == c.get("Name", "Unknown")
        ]

        if not filtered_chargers:
            console.print(
                f"[yellow]No chargers found matching '{show_charger}'[/yellow]"
            )
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:

            charger_task = progress.add_task(
                "Processing chargers...", total=len(filtered_chargers)
            )

            for charger in filtered_chargers:
                charger_name = charger.get("Name", "Unknown")
                progress.update(
                    charger_task, description=f"Processing {charger_name}..."
                )

                # Add progress tracking for API pagination
                fetch_task = progress.add_task(
                    f"Fetching data for {charger_name}...", total=None
                )

                energy_details, charges_count = zaptec.get_energy_history(
                    charger.get("Id"),
                    start_date,
                    end_date,
                    page_size=50,
                    progress=progress,
                    task_id=fetch_task,
                )

                progress.remove_task(fetch_task)

                total_cost = 0.0
                total_energy = 0.0
                if energy_details:
                    energy_task = progress.add_task(
                        f"Calculating costs for {charger_name}...",
                        total=len(energy_details),
                    )

                    for i, energy_detail in enumerate(energy_details):
                        if energy_detail["Energy"] == 0:
                            progress.advance(energy_task)
                            continue

                        dt = datetime.datetime.fromisoformat(energy_detail["Timestamp"])
                        dt = dt - datetime.timedelta(minutes=1)
                        price = mgrey.get_price(dt)
                        energy_detail["Price"] = price
                        cost = energy_detail["Energy"] * price
                        total_energy += energy_detail["Energy"]
                        energy_detail["Cost"] = cost
                        total_cost += cost

                        progress.advance(energy_task)

                    progress.remove_task(energy_task)

                console.print(f"\n[bold]{charger_name}[/bold]")
                console.print(f"Charges: {charges_count}")
                console.print(f"Total energy: {total_energy:.2f} kWh")
                console.print(f"Total cost with hourly rates: {total_cost:.2f} kr")
                console.print(f"Average price per kWh {total_cost / total_energy:.2f}")
                console.print("-" * 40)

                progress.advance(charger_task)

    except Exception as e:
        console.print(f"[red]Error fetching chargers: {e}[/red]")


if __name__ == "__main__":
    fire.Fire(main)
