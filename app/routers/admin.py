import json

from fastapi import APIRouter, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlmodel import col, select

from app.dependencies import AdminDep, SessionDep, profile_completeness
from app.models import LogEntry, User, UserRead

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")


@router.get("/hidden")
def hidden_page(
    request: Request,
    user: AdminDep,
    session: SessionDep,
):
    users = [UserRead.model_validate(u) for u in session.exec(select(User)).all()]
    return templates.TemplateResponse(request, "hidden.html", {"user": user, "users": users})


@router.get("/rating")
def rating_page(
    request: Request,
    user: AdminDep,
    session: SessionDep,
    descending: bool = True,
):
    smtm = select(User).order_by(col(User.username))
    users = [UserRead.model_validate(u) for u in session.exec(smtm).all()]

    rows = [
        {
            "user": u,
            "rating": profile_completeness(u),
        }
        for u in users
    ]
    rows.sort(key=lambda r: r["rating"], reverse=descending)

    return templates.TemplateResponse(request, "rating.html", {"user": user, "rows": rows})


@router.get("/logs")
def logs_page(
    request: Request,
    user: AdminDep,
    session: SessionDep,
):
    logs = session.exec(select(LogEntry).order_by(col(LogEntry.created_at).desc())).all()

    return templates.TemplateResponse(
        request,
        "logs.html",
        {"user": user, "logs": logs},
    )


@router.get("/logs/download", name="download_logs")
def download_logs(
    user: AdminDep,
    session: SessionDep,
):
    logs = session.exec(select(LogEntry).order_by(col(LogEntry.created_at).desc())).all()
    data = [
        {
            "id": log.id,
            "created_at": log.created_at.isoformat(),
            "user": log.user.username if log.user else None,
            "action": log.action,
            "path": log.path,
            "status_code": log.status_code,
        }
        for log in logs
    ]

    return Response(
        content=json.dumps(data, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={
            "Content-Disposition": 'attachment; filename="logs.json"',
        },
    )
