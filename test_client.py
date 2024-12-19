import grpc

import sys
import os
# Add the root project directory to PYTHONPATH 
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

from generated import banner_service_pb2, banner_service_pb2_grpc


def test_get_current_banner(location):
    # Connect to the server
    with grpc.insecure_channel("localhost:51234") as channel:
        stub = banner_service_pb2_grpc.BannerServiceStub(channel)
        
        # Prepare the request
        request = banner_service_pb2.GetCurrentBannerRequest(location=location)
        
        try:
            # Call the method
            response = stub.GetCurrentBanner(request)
            
            # Print the response
            print("Banner Response:")
            print(f"Title: {response.title}")
            print(f"Description: {response.description}")
            print(f"Image Format: {response.image_format}")
            print(f"Image Data Size: {len(response.image)} bytes")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    # Test with different locations
    test_get_current_banner("US")
    test_get_current_banner("FR")
    test_get_current_banner("INVALID_LOCATION")
    test_get_current_banner("GB")
    test_get_current_banner("DE")