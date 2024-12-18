from locust import User, task, between
import grpc
from generated import banner_service_pb2, banner_service_pb2_grpc 

class BannerServiceUser(User):
    wait_time = between(1, 3)  # Simulates users waiting 1 to 3 seconds between actions

    def on_start(self):
        self.channel = grpc.insecure_channel("localhost:51234")
        self.stub = banner_service_pb2_grpc.BannerServiceStub(self.channel)

    @task
    def get_current_banner(self):
        try:
            request = banner_service_pb2.GetCurrentBannerRequest(location="US")
            response = self.stub.GetCurrentBanner(request)
            assert response.title, "Response title should not be empty"
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

    def on_stop(self):
        self.channel.close()
