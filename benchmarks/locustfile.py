from locust import User, task, between
from locust.contrib.fasthttp import FastHttpLocust
import grpc
from generated import banner_service_pb2, banner_service_pb2_grpc


# Add the generated directory to PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

class BannerServiceUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        self.client = grpc.insecure_channel("localhost:51234")
        self.stub = banner_service_pb2_grpc.BannerServiceStub(self.client)

    @task
    def get_current_banner(self):
        with self.client.request_context('BannerService/GetCurrentBanner'):
            try:
                request = banner_service_pb2.GetCurrentBannerRequest(location="US")
                response = self.stub.GetCurrentBanner(request)
                assert response.title, "Title is empty"
            except grpc.RpcError as e:
                self.environment.events.request_failure.fire(
                    request_type="gRPC",
                    name="GetCurrentBanner",
                    response_time=0,
                    exception=e,
                )

    def on_stop(self):
        self.client.close()
