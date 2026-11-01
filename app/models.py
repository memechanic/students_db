from enum import StrEnum

from pydantic import SecretStr
from sqlmodel import Field, SQLModel


class EducationType(StrEnum):
    BACHELOR = "Бакалавриат"
    MASTER = "Магистратура"
    SPECIALIST = "Специалитет"
    PHD = "Аспирантура"


class Faculty(StrEnum):
    ISHPR = "ИШПР"
    ISHE = "ИШЭ"
    ISHYAT = "ИШЯТ"
    ISHNKB = "ИШНКБ"
    ISHITR = "ИШИТР"
    ISHNPT = "ИШНПТ"
    ISHHBMT = "ИШХБМТ"
    ISHB = "ИШБ"
    PISHIES = "ПИШ ИЭС"
    YUTI = "ЮТИ"


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=50)

    full_name: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    bio: str | None = Field(default=None, max_length=500)

    course: int | None = Field(default=None, ge=1, le=6)
    faculty: Faculty | None = Field(default=None)
    education_type: EducationType | None = Field(default=None)

    photo_url: str | None = Field(default=None, max_length=500)
    is_hidden: bool = Field(default=False)

    is_admin: bool = Field(default=False)


class UserRead(UserBase):
    id: int


class UserCreate(SQLModel):
    username: str = Field(min_length=3, max_length=30)
    password: SecretStr = Field(min_length=8)


class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    bio: str | None = Field(default=None, max_length=500)

    course: int | None = Field(default=None, ge=1, le=6)
    faculty: Faculty | None = Field(default=None)
    education_type: EducationType | None = Field(default=None)


class UserLogin(SQLModel):
    username: str
    password: str
    remember_me: bool = False


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
