from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.avatar import delete_avatar, save_avatar
from app.dependencies import OptionalUserDep, RequiredUserDep, SessionDep, UserUpdateDep
from app.models import EducationType, Faculty, User, UserFilter

router = APIRouter()

templates = Jinja2Templates("templates")

templates.env.globals["EducationType"] = EducationType
templates.env.globals["Faculty"] = Faculty


@router.get("/")
def index(
    request: Request,
    user: OptionalUserDep,
    session: SessionDep,
    filter_query: Annotated[UserFilter, Query()],
):
    filters = filter_query.model_dump(exclude_none=True)

    conditions = [User.is_hidden == False]

    for field, value in filters.items():
        column = getattr(User, field)
        if isinstance(value, str) and field not in ["faculty", "education_type"]:
            conditions.append(column.ilike(f"%{value}%"))
        else:
            conditions.append(column == value)

    users = session.exec(select(User).where(*conditions)).all()

    return templates.TemplateResponse(request, "index.html", context={"user": user, "users": users})


@router.get("/profile")
def profile(
    request: Request,
    user: RequiredUserDep,
):
    return templates.TemplateResponse(request, "profile.html", context={"user": user})


@router.get("/profile/edit")
def profile_edit_page(
    request: Request,
    user: RequiredUserDep,
):
    return templates.TemplateResponse(request, "profile_edit.html", context={"user": user})


@router.post("/profile/edit")
def profile_edit(
    user: RequiredUserDep,
    session: SessionDep,
    form: UserUpdateDep,
    photo: Annotated[UploadFile | None, File()] = None,
    delete_icon: Annotated[bool, Form()] = False,
):
    db_user = session.get(User, user.id)
    if db_user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Не существует такого пользователя.",
        )

    db_user.sqlmodel_update(form.model_dump())

    if photo and photo.filename:
        delete_avatar(db_user.photo_url)
        db_user.photo_url = save_avatar(photo)

    elif delete_icon:
        delete_avatar(db_user.photo_url)
        db_user.photo_url = None

    session.add(db_user)
    session.commit()

    return JSONResponse({"redirect": "/profile"})
