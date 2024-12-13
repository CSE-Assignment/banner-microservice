import pytest
from banner_service import BannerService
from banner_config import load_configs
from generated import banner_service_pb2
from datetime import datetime, timezone


@pytest.fixture
def service():
    """
    Provides an instance of the BannerService for testing.
    """
    return BannerService()


def test_get_current_banner_with_image(mocker, service):
    """
    Test that GetCurrentBanner returns the banner with the correct image data.
    """
    mock_banners = load_configs(config_dir="resources/configs")
    mocker.patch("banner_service.banners", mock_banners)

    # Mock the datetime module in banner_service
    mock_datetime = mocker.patch("banner_service.datetime")
    mock_datetime.now.return_value = datetime(2024, 12, 10, tzinfo=timezone.utc)

    request = banner_service_pb2.GetCurrentBannerRequest(location="US")
    response = service.GetCurrentBanner(request, None)

    assert response.title == "Some Sale"
    assert response.description == "End of Season LOOOOOT!"
    assert response.image_format == "png"
    assert response.image


def test_get_current_banner_image_not_found(mocker, service):
    """
    Test that the default banner is returned if the image for a banner is not found.
    """
    mock_banners = load_configs(config_dir="resources/configs")
    mocker.patch("banner_service.banners", mock_banners)

    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    # Mock the datetime module in banner_service
    mock_datetime = mocker.patch("banner_service.datetime")
    mock_datetime.now.return_value = datetime(2024, 12, 10, tzinfo=timezone.utc)

    request = banner_service_pb2.GetCurrentBannerRequest(location="US")
    response = service.GetCurrentBanner(request, None)

    assert response.title == "Default Banner"
    assert response.description == "This is a default banner."
    assert response.image_format == "png"
    assert not response.image  # Default banner has no image
