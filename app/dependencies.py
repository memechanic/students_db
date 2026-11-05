from typing import Annotated

from fastapi import Depends, Form, HTTPException, Request, status
from sqlmodel import Session

from app.database import get_session
from app.models import EducationType, Faculty, User, UserRead, UserUpdate
from app.session_cookie import read_session_cookie

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(
    request: Request,
    session: SessionDep,
) -> UserRead | None:
    user_id = read_session_cookie(request)

    if user_id is None:
        return None

    user = session.get(User, user_id)
    if user is None:
        return None

    return UserRead.model_validate(user)


OptionalUserDep = Annotated[UserRead | None, Depends(get_current_user)]


def get_required_user(user: OptionalUserDep) -> UserRead:
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Не авторизирован")
    return user


RequiredUserDep = Annotated[UserRead, Depends(get_required_user)]


def get_admin(user: RequiredUserDep) -> UserRead:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Нет доступа")
    return user


AdminDep = Annotated[UserRead, Depends(get_admin)]


def get_user_update(
    full_name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone_number: Annotated[str, Form()],
    course: Annotated[int, Form()],
    faculty: Annotated[Faculty, Form()],
    education_type: Annotated[EducationType, Form()],
    bio: Annotated[str | None, Form()] = None,
) -> UserUpdate:
    return UserUpdate(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        bio=bio,
        course=course,
        faculty=faculty,
        education_type=education_type,
    )


UserUpdateDep = Annotated[UserUpdate, Depends(get_user_update)]
