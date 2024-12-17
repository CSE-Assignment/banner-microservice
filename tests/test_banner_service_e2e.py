import grpc
import pytest
from generated import banner_service_pb2, banner_service_pb2_grpc

pytestmark = pytest.mark.e2e

def test_get_current_banner():
    """
    Test the GetCurrentBanner gRPC endpoint by connecting to the running server.
    """
    # Connect to the locally running server
    with grpc.insecure_channel("localhost:51234") as channel:
        stub = banner_service_pb2_grpc.BannerServiceStub(channel)

        # Test with a valid location
        request = banner_service_pb2.GetCurrentBannerRequest(location="US")
        response = stub.GetCurrentBanner(request)

        assert response.title == "Default Banner" or len(response.title) > 0, "Title should not be empty"
        assert response.description == "This is a default banner." or len(response.description) > 0, "Description should not be empty"
        assert response.image_format == "png", "Image format should be 'png'"
        assert isinstance(response.image, bytes), "Image data should be in bytes"

def test_get_current_banner_invalid_location():
    """
    Test the GetCurrentBanner gRPC endpoint with an invalid location.
    """
    # Connect to the locally running server
    with grpc.insecure_channel("localhost:51234") as channel:
        stub = banner_service_pb2_grpc.BannerServiceStub(channel)

        # Test with an invalid location
        request = banner_service_pb2.GetCurrentBannerRequest(location="INVALID")
        response = stub.GetCurrentBanner(request)

        assert response.title == "Default Banner", "Default banner should be returned for invalid location"
        assert response.description == "This is a default banner.", "Default banner description should match"
        assert response.image_format == "png", "Image format should be 'png'"
        assert isinstance(response.image, bytes), "Image data should be in bytes"
