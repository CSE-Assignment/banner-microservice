import os
import json
from datetime import datetime
import logging
from typing import List


class BannerConfig:
    """
    Represents a single banner configuration.

    Attributes:
        id (str): Unique identifier for the banner.
        title (str): Title of the banner.
        description (str): Description of the banner.
        start_time (datetime): Start time of the banner (parsed from ISO 8601 format).
        end_time (datetime): End time of the banner (parsed from ISO 8601 format).
        locations (List[str]): List of locations where the banner is displayed.
    """

    def __init__(self, id: str, title: str, description: str, start_time: str, end_time: str, locations: List[str]):
        self.id = id
        self.title = title
        self.description = description
        self.start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        self.end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        self.locations = locations

    def __repr__(self):
        return f"BannerConfig(id={self.id}, title={self.title}, start_time={self.start_time}, end_time={self.end_time})"


def validate_config(config: dict) -> bool:
    """
    Validates the given configuration dictionary.

    Args:
        config (dict): The configuration dictionary to validate.

    Returns:
        bool: True if the configuration is valid, False otherwise.
    """
    required_keys = {"id", "title", "description", "start_time", "end_time", "locations"}
    if not all(key in config for key in required_keys):
        logging.error(f"Invalid config: Missing keys. Found keys: {config.keys()}")
        return False
    try:
        # Validate ISO 8601 datetime format
        datetime.fromisoformat(config["start_time"].replace("Z", "+00:00"))
        datetime.fromisoformat(config["end_time"].replace("Z", "+00:00"))
    except ValueError as e:
        logging.error(f"Invalid datetime format in config: {e}")
        return False
    return True


def load_configs(config_dir: str = "resources/configs") -> List[BannerConfig]:
    """
    Loads all banner configurations from the specified directory.

    Args:
        config_dir (str): Path to the directory containing configuration files. Defaults to "resources/configs".

    Returns:
        List[BannerConfig]: A list of validated BannerConfig objects.
    """
    logging.info("Loading banner configs.")
    
    configs = []
    if not os.path.exists(config_dir):
        logging.error(f"Config directory {config_dir} does not exist.")
        return configs

    for filename in os.listdir(config_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(config_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    config_data = json.load(file)
                    if validate_config(config_data):
                        configs.append(BannerConfig(**config_data))
                    else:
                        logging.warning(f"Skipping invalid config file: {filename}")
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Error reading file {filename}: {e}")

    return configs


if __name__ == "__main__":
    "For testing the implementation"
    banners = load_configs()
    for banner in banners:
        print(banner)
