import os
import pytest
from banner_config import BannerConfig, validate_config, load_configs
pytestmark = pytest.mark.unit

@pytest.fixture
def example_config():
    """
    Provides a valid example configuration dictionary.
    """
    return {
        "id": "example",
        "title": "Some Sale",
        "description": "End of Season LOOOOOT!",
        "start_time": "2024-12-01T00:00:00Z",
        "end_time": "2024-12-25T23:59:59Z",
        "locations": ["US", "CA", "DE", "FR"]
    }


def test_validate_config_valid(example_config):
    """
    Test that validate_config correctly validates a valid configuration.
    """
    assert validate_config(example_config) is True


def test_validate_config_invalid():
    """
    Test that validate_config fails for missing keys.
    """
    invalid_config = {
        "id": "example",
        "title": "Some Sale",
        # Missing required fields: description, start_time, end_time, locations
    }
    assert validate_config(invalid_config) is False


def test_banner_config_creation(example_config):
    """
    Test that BannerConfig correctly parses a valid configuration.
    """
    banner = BannerConfig(**example_config)
    assert banner.id == "example"
    assert banner.title == "Some Sale"
    assert banner.description == "End of Season LOOOOOT!"
    assert banner.start_time.isoformat() == "2024-12-01T00:00:00+00:00"
    assert banner.end_time.isoformat() == "2024-12-25T23:59:59+00:00"
    assert "US" in banner.locations


def test_load_configs_with_example_file():
    """
    Test that load_configs correctly loads the example.json file.
    """
    configs = load_configs(config_dir="resources/configs")
    assert len(configs) > 0  # Ensure at least one configuration is loaded

    # Verify the example config is loaded
    example_banner = next((b for b in configs if b.id == "example"), None)
    assert example_banner is not None
    assert example_banner.title == "Some Sale"
    assert example_banner.description == "End of Season LOOOOOT!"
    assert "US" in example_banner.locations
    assert "DE" in example_banner.locations
