import grpc
from generated import banner_service_pb2, banner_service_pb2_grpc

def test_banner_service():
    """Test the deployed banner service."""
    channel = grpc.insecure_channel("bannerservice:51234")
    client = banner_service_pb2_grpc.BannerServiceStub(channel)

    # Send a request
    request = banner_service_pb2.GetCurrentBannerRequest(location="US")
    response = client.GetCurrentBanner(request)

    # Validate
    print(f"Title: {response.title}")
    print(f"Description: {response.description}")
    assert response.title
    assert response.description
