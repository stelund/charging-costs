import os
import json
from pathlib import Path
from getpass import getpass

CONFIG_FILE = Path.home() / ".charging-costs" / "config.json"


def ensure_config_dir():
    """Ensure the config directory exists."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        return {}

    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(config: dict):
    """Save configuration to file."""
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_zaptec_credentials() -> tuple[str, str]:
    """Get Zaptec credentials from environment variables or config file, prompting if needed."""
    # Try environment variables first
    username = os.getenv("ZAPTEC_USERNAME")
    password = os.getenv("ZAPTEC_PASSWORD")

    if username and password:
        return username, password

    # Try config file
    config = load_config()
    username = config.get("zaptec_username")
    password = config.get("zaptec_password")

    if username and password:
        return username, password

    # Prompt for credentials
    print("Zaptec credentials not found. Please enter them below:")
    username = input("Zaptec username: ").strip()
    password = getpass("Zaptec password: ").strip()

    if not username or not password:
        raise ValueError("Username and password are required")

    # Save to config file
    config["zaptec_username"] = username
    config["zaptec_password"] = password
    save_config(config)

    print(f"Credentials saved to {CONFIG_FILE}")
    return username, password


def get_zaptec_base_url() -> str:
    """Get Zaptec base URL from environment or config."""
    url = os.getenv("ZAPTEC_BASE_URL")
    if url:
        return url

    config = load_config()
    return config.get("zaptec_base_url", "https://api.zaptec.com")
