import pytest
from unittest.mock import patch, mock_open
from datetime import datetime, timezone
from banner_service import BannerService
from banner_config import load_configs
from generated.banner_service_pb2 import GetCurrentBannerRequest


@pytest.fixture
def service():
    """
    Provides a BannerService instance for testing.
    """
    return BannerService()


def test_get_current_banner_with_image(mocker, service):
    """
    Test that GetCurrentBanner returns the banner with the correct image data.
    """
    # Load banner from example.json
    mock_banners = load_configs(config_dir="resources/configs")
    mocker.patch("banner_service.banners", mock_banners)

    # Mock the current time to fall within the banner's time range
    mocker.patch("banner_service.datetime.now", return_value=datetime(2024, 12, 10, tzinfo=timezone.utc))

    # Mock image file reading
    image_path = "resources/content/example.png"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    mocker.patch("builtins.open", mock_open(read_data=image_data))

    # A valid location request
    request = GetCurrentBannerRequest(location="US")
    response = service.GetCurrentBanner(request, None)

    # Verify response
    assert response.title == "Some Sale"
    assert response.description == "End of Season LOOOOOT!"
    assert response.image == image_data
    assert response.image_format == "png"


def test_get_current_banner_image_not_found(mocker, service):
    """
    Test that the default banner is returned if the image for a banner is not found.
    """
    # Load banner from example.json
    mock_banners = load_configs(config_dir="resources/configs")
    mocker.patch("banner_service.banners", mock_banners)

    # Mock the file open to simulate a missing image file
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    # Mock the current time to fall within the banner's time range
    mocker.patch("banner_service.datetime.now", return_value=datetime(2024, 12, 10, tzinfo=timezone.utc))

    # Create a request for a valid location
    request = GetCurrentBannerRequest(location="US")
    response = service.GetCurrentBanner(request, None)

    # Verify the default banner is returned due to the missing image
    assert response.title == "Default Banner"
    assert response.description == "This is a default banner."
    assert response.image == b""  # No image loaded
    assert response.image_format == "png"
