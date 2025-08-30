import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
import pytest
import config


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = Path(f.name)
    
    original_config_file = config.CONFIG_FILE
    config.CONFIG_FILE = temp_path
    
    yield temp_path
    
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()
    config.CONFIG_FILE = original_config_file


def test_load_config_nonexistent_file(temp_config_file):
    """Test loading config when file doesn't exist."""
    result = config.load_config()
    assert result == {}


def test_load_config_existing_file(temp_config_file):
    """Test loading config from existing file."""
    test_config = {"zaptec_username": "test_user", "zaptec_password": "test_pass"}
    
    with open(temp_config_file, "w") as f:
        json.dump(test_config, f)
    
    result = config.load_config()
    assert result == test_config


def test_save_config(temp_config_file):
    """Test saving config to file."""
    test_config = {"zaptec_username": "test_user", "zaptec_password": "test_pass"}
    
    config.save_config(test_config)
    
    with open(temp_config_file, "r") as f:
        saved_config = json.load(f)
    
    assert saved_config == test_config


@patch.dict(os.environ, {"ZAPTEC_USERNAME": "env_user", "ZAPTEC_PASSWORD": "env_pass"})
def test_get_zaptec_credentials_from_env():
    """Test getting credentials from environment variables."""
    username, password = config.get_zaptec_credentials()
    assert username == "env_user"
    assert password == "env_pass"


def test_get_zaptec_credentials_from_config(temp_config_file):
    """Test getting credentials from config file."""
    test_config = {"zaptec_username": "config_user", "zaptec_password": "config_pass"}
    config.save_config(test_config)
    
    username, password = config.get_zaptec_credentials()
    assert username == "config_user"
    assert password == "config_pass"


@patch.dict(os.environ, {}, clear=True)  # Clear all env vars
@patch('config.input', return_value="prompt_user")
@patch('config.getpass', return_value="prompt_pass")
def test_get_zaptec_credentials_prompt_and_save(mock_getpass, mock_input, temp_config_file):
    """Test prompting for credentials and saving them."""
    username, password = config.get_zaptec_credentials()
    
    assert username == "prompt_user"
    assert password == "prompt_pass"
    
    # Verify credentials were saved
    saved_config = config.load_config()
    assert saved_config["zaptec_username"] == "prompt_user"
    assert saved_config["zaptec_password"] == "prompt_pass"


@patch.dict(os.environ, {}, clear=True)  # Clear all env vars
@patch('config.input', return_value="")
@patch('config.getpass', return_value="")
def test_get_zaptec_credentials_empty_input(mock_getpass, mock_input, temp_config_file):
    """Test error when empty credentials are provided."""
    with pytest.raises(ValueError, match="Username and password are required"):
        config.get_zaptec_credentials()


@patch.dict(os.environ, {"ZAPTEC_BASE_URL": "https://custom.api.com"})
def test_get_zaptec_base_url_from_env():
    """Test getting base URL from environment variable."""
    url = config.get_zaptec_base_url()
    assert url == "https://custom.api.com"


def test_get_zaptec_base_url_default(temp_config_file):
    """Test getting default base URL."""
    url = config.get_zaptec_base_url()
    assert url == "https://api.zaptec.com"


def test_get_zaptec_base_url_from_config(temp_config_file):
    """Test getting base URL from config file."""
    test_config = {"zaptec_base_url": "https://config.api.com"}
    config.save_config(test_config)
    
    url = config.get_zaptec_base_url()
    assert url == "https://config.api.com"