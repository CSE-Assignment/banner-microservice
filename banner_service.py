import grpc
from typing import Optional
from grpc import ServicerContext
from concurrent import futures
import logging
from datetime import datetime, timezone

import sys
import os
# Add the root project directory to PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

from generated import banner_service_pb2, banner_service_pb2_grpc
from banner_config import load_configs, BannerConfig


# Load all banner configurations
banners = load_configs()

DEFAULT_BANNER = BannerConfig(
    id="default",
    title="Default Banner",
    description="This is a default banner.",
    start_time="2000-01-01T00:00:00Z",
    end_time="2100-01-01T00:00:00Z",
    locations=["ALL"]
)


class BannerService(banner_service_pb2_grpc.BannerServiceServicer):
    def GetCurrentBanner(
        self, 
        request: banner_service_pb2.GetCurrentBannerRequest, 
        context: ServicerContext
    ) -> banner_service_pb2.GetCurrentBannerResponse:
        """
        Handle the GetCurrentBanner gRPC request.

        Args:
            request (GetCurrentBannerRequest): The incoming gRPC request containing the location.
            context (ServicerContext): The context of the gRPC call.

        Returns:
            GetCurrentBannerResponse: The response with banner data, based on time and location.
        """
        # Extract location and current time
        location = request.location
        current_time = datetime.now(timezone.utc)

        # Filter banners based on time and location
        matching_banners = [
            banner for banner in banners
            if banner.start_time <= current_time <= banner.end_time and
               (location in banner.locations or "ALL" in banner.locations) and
               self._is_special_condition_met(banner.special_condition, current_time)
        ]

        if not matching_banners:
            logging.error("No matching banners found. Returning default banner.")
            return self._create_response(DEFAULT_BANNER, "png")
        
        if len(matching_banners) > 1:
            logging.warning(f"Multiple banners match the criteria. Choosing the first one: {matching_banners[0].id}")

        # Choose the first matching banner
        selected_banner = matching_banners[0]

        # Prepare image path and read image data
        image_path = f"resources/content/{selected_banner.id}.png"
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
        except FileNotFoundError:
            logging.error(f"Image not found for banner ID {selected_banner.id}. Returning default banner.")
            return self._create_response(DEFAULT_BANNER, "png")

        return self._create_response(selected_banner, "png", image_data)

    def _is_special_condition_met(self, special_condition: str|None, current_time: datetime) -> bool:
        """
        Evaluate if the special condition for a banner is met.

        Args:
            special_condition (str): The special condition to evaluate.
            current_time (datetime): The current time to evaluate against.

        Returns:
            bool: True if the condition is met, otherwise False.
        """
        if not special_condition:
            return True  # No special condition means always valid
        
        match special_condition:
            case "odd-minutes":
                return current_time.minute % 2 != 0
            case "even-minutes":
                return current_time.minute % 2 == 0
            case _:
                logging.warning(f"Unrecognized special condition: {special_condition}")
                return False

    def _create_response(
        self, 
        banner: BannerConfig, 
        image_format: str, 
        image_data: Optional[bytes] = None
    ) -> banner_service_pb2.GetCurrentBannerResponse:
        """
        Create a GetCurrentBannerResponse object.

        Args:
            banner (BannerConfig): The banner configuration to include in the response.
            image_format (str): The format of the image (e.g., 'png').
            image_data (Optional[bytes]): The image data in bytes.

        Returns:
            GetCurrentBannerResponse: The response with banner data.
        """
        # Return response with banner data
        return banner_service_pb2.GetCurrentBannerResponse(
            title=banner.title,
            description=banner.description,
            image=image_data or b"",  # Default empty image if not found
            image_format=image_format
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    banner_service_pb2_grpc.add_BannerServiceServicer_to_server(BannerService(), server)
    server.add_insecure_port("[::]:51234")
    logging.info("Starting gRPC server on port 51234...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
