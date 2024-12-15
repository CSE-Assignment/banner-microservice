import pytest
from unittest.mock import mock_open
from generated import banner_service_pb2
from banner_service import BannerService
from banner_config import BannerConfig
from datetime import datetime, timezone

pytestmark = pytest.mark.component

@pytest.fixture
def service():
    """Provides an instance of the BannerService."""
    return BannerService()

def test_grpc_get_current_banner(mocker, service):
    """Test the gRPC GetCurrentBanner API."""
    # Mock the banners
    mock_banners = [
        BannerConfig(
            id="test_banner",
            title="Test Banner",
            description="Test Description",
            start_time="2024-12-01T00:00:00Z",
            end_time="2024-12-31T23:59:59Z",
            locations=["US", "CA"]
        )
    ]
    mocker.patch("banner_service.banners", mock_banners)

    # Mock datetime.now
    mock_datetime = mocker.patch("banner_service.datetime")
    mock_datetime.now.return_value = datetime(2024, 12, 10, tzinfo=timezone.utc)

    # Mock file open for the banner image
    mock_file = mock_open(read_data=b"mock_image_data")
    mocker.patch("builtins.open", mock_file)

    request = banner_service_pb2.GetCurrentBannerRequest(location="US")
    response = service.GetCurrentBanner(request, None)

    assert response.title == "Test Banner"
    assert response.description == "Test Description"
    assert response.image == b"mock_image_data" 

def test_missing_banner_image(mocker, service):
    """Test that the default banner is returned if the image file is missing."""
    # Mock the config
    mock_banners = [
        BannerConfig(
            id="test_banner",
            title="Test Banner",
            description="Test Description",
            start_time="2024-12-01T00:00:00Z",
            end_time="2024-12-31T23:59:59Z",
            locations=["US", "CA"]
        )
    ]
    mocker.patch("banner_service.banners", mock_banners)

    # Mock the datetime module
    mock_datetime = mocker.patch("banner_service.datetime")
    mock_datetime.now.return_value = datetime(2024, 12, 10, tzinfo=timezone.utc)

    # Mock the file open to simulate a missing image file
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    request = banner_service_pb2.GetCurrentBannerRequest(location="US")
    response = service.GetCurrentBanner(request, None)

    assert response.title == "Default Banner"
    assert response.description == "This is a default banner."
