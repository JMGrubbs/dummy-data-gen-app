import asyncio
from typing import Any

import httpx


async def process_data_gen_task_async(
    task_id: int,
    data: dict[str, Any],
) -> None:
    request_count = int(data.get("remaining_requests", 0))
    requests_per_min = max(int(data.get("requests_per_min", 60)), 1)
    url = data.get("url_destination")
    payload = data.get("data_bp", {})

    if request_count <= 0:
        return

    if not url:
        raise ValueError(f"Task {task_id} has no destination URL.")

    delay_seconds = 60 / requests_per_min

    async with httpx.AsyncClient(timeout=10.0) as client:
        for request_number in range(1, request_count + 1):
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                print(f"Task {task_id}: request {request_number}/{request_count} succeeded ({response.status_code})")
            except httpx.HTTPStatusError as exc:
                print(f"Task {task_id}: request {request_number}/{request_count} failed ({exc.response.status_code})")
            except httpx.RequestError as exc:
                print(f"Task {task_id}: request {request_number}/{request_count} failed: {exc}")

            if request_number < request_count:
                await asyncio.sleep(delay_seconds)
