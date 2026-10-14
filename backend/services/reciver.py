import asyncio

from core.config import settings
from httpx import Response
from httpxC.http_client import http_client


async def send_data_to_reciver(data: dict) -> None:
    reciver_url: str = f"{settings.reciver_url}/api/v1/reciver/hook"
    number_of_requests: int = data.get("number_of_requests", 5)
    requests_per_min: int = data.get("requests_per_min", 60)

    while number_of_requests > 0:
        request_package: dict = data
        request_package["remaining"] = number_of_requests
        try:
            response: Response = await http_client.post(reciver_url, json=request_package)
            response.raise_for_status()
        except Exception as e:
            print(f"Error sending data to reciver: {e}")
        finally:
            number_of_requests -= 1
            if number_of_requests > 0:
                await asyncio.sleep(60 / requests_per_min)
