# middleware.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from src.services.refresh_token import refresh_kubectl_token

class RefreshTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Call the function to refresh the kubectl token
        refresh_kubectl_token()
        # Proceed with the request
        response = await call_next(request)
        return response
