from locust import User, task, between
import grpc
import sys
import os
import time

# Add the generated directory to PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

from generated import banner_service_pb2, banner_service_pb2_grpc


class BannerServiceUser(User):
    wait_time = between(1, 3)  # Simulates users waiting 1 to 3 seconds between actions

    def on_start(self):
        """
        Establish the gRPC channel and stub when the user starts.
        """
        self.channel = grpc.insecure_channel("localhost:51234")
        self.stub = banner_service_pb2_grpc.BannerServiceStub(self.channel)

    @task
    def get_current_banner(self):
        """
        Task to call the GetCurrentBanner endpoint for different locations.
        Logs requests as successes or failures for Locust tracking.
        """
        locations = ["US", "FR", "INVALID_LOCATION", "GB", "DE"]
        for location in locations:
            request = banner_service_pb2.GetCurrentBannerRequest(location=location)
            start_time = time.time()  # Start time for tracking response duration
            try:
                # Call the gRPC method
                response = self.stub.GetCurrentBanner(request)
                response_time = (time.time() - start_time) * 1000  # Response time in milliseconds

                # Log successful requests
                self.environment.events.request.fire(
                    request_type="gRPC",
                    name=f"GetCurrentBanner-{location}",
                    response_time=response_time,
                    response_length=len(response.image),
                    exception=None,
                )
                print("Banner Response:")
                print(f"Title: {response.title}")
                print(f"Description: {response.description}")
                print(f"Image Format: {response.image_format}")
                print(f"Image Data Size: {len(response.image)} bytes")

            except grpc.RpcError as e:
                response_time = (time.time() - start_time) * 1000  # Response time in milliseconds

                # Log failed requests
                self.environment.events.request.fire(
                    request_type="gRPC",
                    name=f"GetCurrentBanner-{location}",
                    response_time=response_time,
                    response_length=0,
                    exception=e,
                )
                print(f"gRPC error for location {location}: {e.code()} - {e.details()}")

    def on_stop(self):
        """
        Close the gRPC channel when the user stops.
        """
        self.channel.close()
