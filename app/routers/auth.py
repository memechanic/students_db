from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.dependencies import SessionDep
from app.models import User, UserCreate, UserLogin
from app.security import get_password_hash, verify_password
from app.session_cookie import SESSION_COOKIE, create_session_cookie

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# -------------------- Регистрация -------------------- #


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


@router.post("/register")
def register(
    user: Annotated[UserCreate, Form()],
    session: SessionDep,
):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким именем уже существует",
        )

    new_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password.get_secret_value()),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    if new_user.id is None:
        raise RuntimeError("Created user has no id")

    response = JSONResponse({"redirect": "/profile/edit"}, status_code=status.HTTP_201_CREATED)
    create_session_cookie(response, new_user.id, persistent=False)
    return response


# -------------------- Авторизация -------------------- #


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request, name="login.html")


@router.post("/login")
def login(
    data: Annotated[UserLogin, Form()],
    session: SessionDep,
):

    db_user = session.exec(select(User).where(User.username == data.username)).first()

    if db_user is None or not verify_password(data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )

    if db_user.id is None:
        raise RuntimeError("Existing user has no id")
    response = JSONResponse({"redirect": "/"})
    create_session_cookie(response, db_user.id, persistent=data.remember_me)
    return response


@router.get("/logout")
@router.post("/logout")
def logout():
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(SESSION_COOKIE)
    return response
