from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.dependencies import AdminDep, SessionDep
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/hidden")
def hidden_page(
    request: Request,
    user: AdminDep,
    session: SessionDep,
):
    users = session.exec(select(User)).all()
    return templates.TemplateResponse(request, "hidden.html", {"user": user, "users": users})
