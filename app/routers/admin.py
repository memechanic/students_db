from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import col, select

from app.dependencies import AdminDep, SessionDep
from app.models import User

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")


@router.get("/hidden")
def hidden_page(
    request: Request,
    user: AdminDep,
    session: SessionDep,
):
    # TODO: Провалидировать пользователей UserRead
    users = session.exec(select(User)).all()
    return templates.TemplateResponse(request, "hidden.html", {"user": user, "users": users})


@router.get("/rating")
def rating_page(
    request: Request,
    user: AdminDep,
    session: SessionDep,
):
    # TODO: Провалидировать пользователей UserRead
    users = session.exec(
        select(User).order_by(
            col(User.rating).desc(),
            col(User.username),
        )
    ).all()
    return templates.TemplateResponse(request, "rating.html", {"user": user, "users": users})
