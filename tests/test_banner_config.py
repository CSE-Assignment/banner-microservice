import os
import pytest
import json
from datetime import datetime
from banner_config import BannerConfig, validate_config, load_configs


@pytest.fixture
def valid_config():
    return {
        "id": "1",
        "title": "Black Friday Sale",
        "description": "Big discounts available!",
        "start_time": "2024-11-24T00:00:00Z",
        "end_time": "2024-11-30T23:59:59Z",
        "locations": ["New York", "Los Angeles"]
    }


@pytest.fixture
def invalid_config_missing_keys():
    return {
        "id": "1",
        "title": "Black Friday Sale",
        # Missing description, start_time, end_time, locations
    }


@pytest.fixture
def invalid_config_invalid_datetime():
    return {
        "id": "1",
        "title": "Black Friday Sale",
        "description": "Big discounts available!",
        "start_time": "invalid-date",
        "end_time": "2024-11-30T23:59:59Z",
        "locations": ["New York", "Los Angeles"]
    }


def test_banner_config_creation(valid_config):
    banner = BannerConfig(**valid_config)
    assert banner.id == "1"
    assert banner.title == "Black Friday Sale"
    assert banner.start_time == datetime.fromisoformat("2024-11-24T00:00:00+00:00")
    assert banner.locations == ["New York", "Los Angeles"]


def test_validate_config_success(valid_config):
    assert validate_config(valid_config) is True


def test_validate_config_missing_keys(invalid_config_missing_keys):
    assert validate_config(invalid_config_missing_keys) is False


def test_validate_config_invalid_datetime(invalid_config_invalid_datetime):
    assert validate_config(invalid_config_invalid_datetime) is False


def test_load_configs_valid(mocker, valid_config, tmpdir):
    # Create temporary config directory
    config_dir = tmpdir.mkdir("configs")
    config_file = config_dir.join("valid_config.json")

    # Write valid config to a file
    config_file.write(json.dumps(valid_config))

    # Mock `os.listdir` to return the temporary file
    mocker.patch("os.listdir", return_value=[config_file.basename])
    mocker.patch("os.path.exists", return_value=True)

    configs = load_configs(config_dir=str(config_dir))
    assert len(configs) == 1
    assert configs[0].id == "1"
    assert configs[0].title == "Black Friday Sale"


def test_load_configs_invalid(mocker, invalid_config_missing_keys, tmpdir):
    # Create temporary config directory
    config_dir = tmpdir.mkdir("configs")
    config_file = config_dir.join("invalid_config.json")

    # Write invalid config to a file
    config_file.write(json.dumps(invalid_config_missing_keys))

    # Mock `os.listdir` to return the temporary file
    mocker.patch("os.listdir", return_value=[config_file.basename])
    mocker.patch("os.path.exists", return_value=True)

    configs = load_configs(config_dir=str(config_dir))
    assert len(configs) == 0  # No valid configs should be loaded
