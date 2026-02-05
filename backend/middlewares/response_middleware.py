from typing import Callable
from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
import json

class UniformRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(request)

            if isinstance(response, JSONResponse):
                try:
                    # Access the rendered content (bytes) and load it as JSON
                    data = json.loads(response.body)
                except (json.JSONDecodeError, TypeError):
                    # Handle cases where body is not valid JSON or not bytes
                    data = None
            else:
                # For other response types, we need to await the body
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                try:
                    data = json.loads(body) if body else None
                except (json.JSONDecodeError, TypeError):
                    data = None

            # For successful responses, wrap data
            if 200 <= response.status_code < 300:
                return JSONResponse(
                    content={"status": "success", "data": data, "error": ""},
                    status_code=response.status_code,
                )

            # For error responses, format the error
            return JSONResponse(
                content={"status": "error", "data": None, "error": data.get("detail", str(data)) if data else "An error occurred"},
                status_code=response.status_code,
            )

        return custom_route_handler