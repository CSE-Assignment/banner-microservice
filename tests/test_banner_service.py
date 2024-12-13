import pytest
from datetime import datetime, timezone
from unittest.mock import patch, mock_open
from grpc import ServicerContext
from generated.banner_service_pb2 import GetCurrentBannerRequest, GetCurrentBannerResponse
from banner_service import BannerService, DEFAULT_BANNER, banners


@pytest.fixture
def service():
    return BannerService()


@pytest.fixture
def mock_banners():
    """
    Mock banner configurations for testing.
    """
    return [
        DEFAULT_BANNER,
        BannerConfig(
            id="holiday",
            title="Holiday Sale",
            description="Discounts for the holiday season!",
            start_time="2024-12-01T00:00:00Z",
            end_time="2024-12-31T23:59:59Z",
            locations=["New York"]
        )
    ]


def test_get_current_banner_default(service, mock_banners, mocker):
    """
    Test that the default banner is returned when no banners match.
    """
    mocker.patch("banner_service.banners", mock_banners)
    request = GetCurrentBannerRequest(location="Unknown")
    response = service.GetCurrentBanner(request, ServicerContext())

    assert response.title == DEFAULT_BANNER.title
    assert response.description == DEFAULT_BANNER.description
    assert response.image == b""  # Default empty image


def test_get_current_banner_matching_banner(service, mock_banners, mocker):
    """
    Test that a matching banner is returned based on location and time.
    """
    mocker.patch("banner_service.banners", mock_banners)
    mocker.patch("banner_service.datetime", wraps=datetime)
    mocker.patch("banner_service.datetime.now", return_value=datetime(2024, 12, 15, tzinfo=timezone.utc))

    request = GetCurrentBannerRequest(location="New York")
    response = service.GetCurrentBanner(request, ServicerContext())

    assert response.title == "Holiday Sale"
    assert response.description == "Discounts for the holiday season!"
    assert response.image == b""  # Since no image mock is provided


def test_get_current_banner_no_image(service, mock_banners, mocker):
    """
    Test that the default banner is returned if the image for a matching banner is not found.
    """
    mocker.patch("banner_service.banners", mock_banners)
    mocker.patch("banner_service.datetime.now", return_value=datetime(2024, 12, 15, tzinfo=timezone.utc))

    # Mock the open function to raise FileNotFoundError
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    request = GetCurrentBannerRequest(location="New York")
    response = service.GetCurrentBanner(request, ServicerContext())

    assert response.title == DEFAULT_BANNER.title
    assert response.description == DEFAULT_BANNER.description
    assert response.image == b""  # Default empty image


def test_get_current_banner_multiple_banners(service, mocker):
    """
    Test that the first matching banner is selected when multiple banners match.
    """
    multiple_banners = [
        BannerConfig(
            id="sale1",
            title="Sale 1",
            description="First sale",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-12-31T23:59:59Z",
            locations=["ALL"]
        ),
        BannerConfig(
            id="sale2",
            title="Sale 2",
            description="Second sale",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-12-31T23:59:59Z",
            locations=["ALL"]
        )
    ]
    mocker.patch("banner_service.banners", multiple_banners)
    mocker.patch("banner_service.datetime.now", return_value=datetime(2024, 7, 15, tzinfo=timezone.utc))

    request = GetCurrentBannerRequest(location="Anywhere")
    response = service.GetCurrentBanner(request, ServicerContext())

    assert response.title == "Sale 1"  # The first matching banner should be selected


def test_create_response(service):
    """
    Test the _create_response method.
    """
    banner = DEFAULT_BANNER
    response = service._create_response(banner, "png")

    assert response.title == banner.title
    assert response.description == banner.description
    assert response.image_format == "png"
    assert response.image == b""
