import logging
from datetime import datetime

from fastapi import Request
from sqlmodel import Session

from app.database import engine
from app.models import LogEntry

ACTION_BY_ROUTE = {
    "/": {
        "GET": "Просмотр главной страницы",
    },
    "/register": {
        "GET": "Просмотр страницы регистрации",
        "POST": "Регистрация пользователя",
    },
    "/login": {
        "GET": "Просмотр страницы входа",
        "POST": "Вход пользователя",
    },
    "/logout": {
        "GET": "Выход пользователя",
        "POST": "Выход пользователя",
    },
    "/profile": {
        "GET": "Просмотр профиля",
    },
    "/profile/edit": {
        "GET": "Просмотр страницы редактирования профиля",
        "POST": "Изменение профиля",
    },
    "/admin/hidden": {
        "GET": "Просмотр полного списка пользователей",
    },
    "/admin/rating": {
        "GET": "Просмотр рейтинга пользователей",
    },
    "/admin/logs": {
        "GET": "Просмотр журнала действий",
    },
    "/admin/logs/download": {
        "GET": "Скачивание журнала действий",
    },
}

SKIP_PREFIXES = (
    "/static/",
    "/media/",
    "/favicon.ico",
    "/docs",
    "/openapi.json",
)


class DatabaseHandler(logging.Handler):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    def emit(self, record: logging.LogRecord):
        if not hasattr(record, "action"):
            return
        try:
            with Session(self.engine) as session:
                newLogEntry = LogEntry(
                    created_at=datetime.fromtimestamp(
                        record.created, datetime.now().astimezone().tzinfo
                    ),
                    user_id=getattr(record, "user_id", None),
                    action=getattr(record, "action", None),
                    path=getattr(record, "path", None),
                    status_code=getattr(record, "status_code", None),
                )
                session.add(newLogEntry)
                session.commit()
        except Exception:  # noqa: BLE001
            self.handleError(record)


logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if len(logger.handlers) == 0:
    logger.addHandler(DatabaseHandler(engine))
logger.propagate = False  # No parent


async def log_requests(request: Request, call_next):
    if request.url.path.startswith(SKIP_PREFIXES):
        return await call_next(request)

    response = await call_next(request)

    action = ACTION_BY_ROUTE.get(request.url.path, {}).get(request.method)
    if action is None:
        return response

    logger.info(
        "Action: %s, Path: %s, Status Code: %d",
        *[action, request.url.path, response.status_code],
        extra={
            "user_id": getattr(request.state, "user_id", None),
            "action": action,
            "path": request.url.path,
            "status_code": response.status_code,
        },
    )
    return response
