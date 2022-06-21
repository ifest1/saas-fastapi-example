import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AnonymousUserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        session_data = request.session.get("session_data")
        if not session_data:
            request.session["session_data"] = {"cart_id": str(uuid.uuid4())}

        return await call_next(request)
