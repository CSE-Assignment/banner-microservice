import grpc
import pytest
import sys
import os
from generated import banner_service_pb2, banner_service_pb2_grpc

pytestmark = pytest.mark.e2e

@pytest.fixture(scope="module")
def grpc_channel():
    """
    Fixture to create a gRPC channel to the running server.
    """
    with grpc.insecure_channel("localhost:51234") as channel:
        yield channel

@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    """
    Fixture to create a gRPC stub for the BannerService.
    """
    return banner_service_pb2_grpc.BannerServiceStub(grpc_channel)

def test_get_current_banner(grpc_stub):
    """
    Test the GetCurrentBanner gRPC endpoint with a valid location.
    """
    # Test with a valid location
    request = banner_service_pb2.GetCurrentBannerRequest(location="US")
    response = grpc_stub.GetCurrentBanner(request)

    assert response.title == "Default Banner" or len(response.title) > 0, "Title should not be empty"
    assert response.description == "This is a default banner." or len(response.description) > 0, "Description should not be empty"
    assert response.image_format == "png", "Image format should be 'png'"
    assert isinstance(response.image, bytes), "Image data should be in bytes"

def test_get_current_banner_invalid_location(grpc_stub):
    """
    Test the GetCurrentBanner gRPC endpoint with an invalid location.
    """
    # Test with an invalid location
    request = banner_service_pb2.GetCurrentBannerRequest(location="INVALID")
    response = grpc_stub.GetCurrentBanner(request)

    assert response.title == "Default Banner", "Default banner should be returned for invalid location"
    assert response.description == "This is a default banner.", "Default banner description should match"
    assert response.image_format == "png", "Image format should be 'png'"
    assert isinstance(response.image, bytes), "Image data should be in bytes"
