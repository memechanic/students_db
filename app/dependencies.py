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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


RequiredUserDep = Annotated[UserRead, Depends(get_required_user)]


# Можно сделать зависимость для админа


def get_user_update(
    full_name: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    phone_number: Annotated[str | None, Form()] = None,
    bio: Annotated[str | None, Form()] = None,
    course: Annotated[int | None, Form()] = None,
    faculty: Annotated[Faculty | None, Form()] = None,
    education_type: Annotated[EducationType | None, Form()] = None,
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
