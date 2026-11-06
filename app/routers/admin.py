from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import col, select

from app.dependencies import AdminDep, SessionDep, profile_completeness
from app.models import User, UserRead

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
