from fastapi import Request, Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.settings import settings

SESSION_COOKIE = "session_token"
WEEK = 60 * 60 * 24 * 7

serializer = URLSafeTimedSerializer(settings.secret_key, salt=SESSION_COOKIE)


def create_session_cookie(response: Response, user_id: int, persistent: bool) -> None:
    token = serializer.dumps({"user_id": user_id})
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=WEEK if persistent else None,
        httponly=True,
        samesite="lax",
    )


def read_session_cookie(request: Request) -> int | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None

    try:
        data: dict = serializer.loads(token, max_age=WEEK)

    except (SignatureExpired, BadSignature):
        return None

    user_id = data.get("user_id")
    if not isinstance(user_id, int):
        return None

    return user_id
