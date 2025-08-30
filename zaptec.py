import requests
import datetime
from typing import Optional
from rich.progress import Progress
import config

_token: Optional[str] = None


def get_token() -> str:
    global _token
    if _token:
        return _token

    username, password = config.get_zaptec_credentials()
    base_url = config.get_zaptec_base_url()

    token_url = f"{base_url}/oauth/token"

    data = {"grant_type": "password", "username": username, "password": password}

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    token_data = response.json()
    _token = token_data["access_token"]
    return _token


def get_headers() -> dict[str, str]:
    token = get_token()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def make_authenticated_request(
    method: str, endpoint: str, **kwargs
) -> requests.Response:
    base_url = config.get_zaptec_base_url()
    url = f"{base_url}{endpoint}"
    headers = get_headers()

    if "headers" in kwargs:
        headers.update(kwargs.pop("headers"))

    return requests.request(method, url, headers=headers, **kwargs)


def list_chargers() -> list[dict]:
    response = make_authenticated_request("GET", "/api/chargers")
    response.raise_for_status()
    data = response.json()
    return data.get("Data", [])


def get_energy_history(
    charger_id: str,
    from_date: datetime.datetime,
    to_date: datetime.datetime,
    page_size: int = 10,
    progress: Optional[Progress] = None,
    task_id: Optional[int] = None,
) -> dict:
    energy_history = []
    charges_count = 0
    page_index = 0

    while True:
        params = {
            "ChargerId": charger_id,
            "From": from_date.isoformat(),
            "To": to_date.isoformat(),
            "PageSize": page_size,
            "PageIndex": page_index,
            "DetailLevel": 1,
        }
        response = make_authenticated_request(
            "GET", "/api/chargehistory", params=params
        )
        response.raise_for_status()
        body = response.json()
        for session in body["Data"]:
            charges_count += 1
            for energy_detail in session.get("EnergyDetails", []):
                energy_history.append(energy_detail)

        page_index += 1

        if progress and task_id is not None:
            progress.advance(task_id)

        if page_index == body["Pages"]:
            break

    return energy_history, charges_count
