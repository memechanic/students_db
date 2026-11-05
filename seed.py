import random

from sqlmodel import Session

from app.database import engine, init_db
from app.models import EducationType, Faculty, User
from app.security import get_password_hash

BACHELOR = EducationType.BACHELOR
MASTER = EducationType.MASTER
SPECIALIST = EducationType.SPECIALIST
PHD = EducationType.PHD

ISHPR = Faculty.ISHPR
ISHE = Faculty.ISHE
ISHYAT = Faculty.ISHYAT
ISHNKB = Faculty.ISHNKB
ISHITR = Faculty.ISHITR
ISHNPT = Faculty.ISHNPT
ISHHBMT = Faculty.ISHHBMT
ISHB = Faculty.ISHB
PISHIES = Faculty.PISHIES
YUTI = Faculty.YUTI

USERS = [
    {
        "username": "ivanov",
        "full_name": "Иван Иванов",
        "email": "ivanov@gmail.com",
        "phone_number": "+79123456789",
        "bio": "Люблю программирование.",
        "course": 4,
        "faculty": ISHPR,
        "education_type": BACHELOR,
        "is_hidden": False,
    },
    {
        "username": "petrova",
        "full_name": "Анна Петрова",
        "email": "petrova@gmail.com",
        "phone_number": "89121234567",
        "bio": "Изучаю дизайн и интерфейсы.",
        "course": 2,
        "faculty": ISHE,
        "education_type": MASTER,
        "is_hidden": False,
    },
    {
        "username": "sidorov",
        "full_name": "Павел Сидоров",
        "email": "sidorov@gmail.com",
        "phone_number": "+79129876543",
        "bio": "Увлекаюсь робототехникой.",
        "course": 6,
        "faculty": ISHYAT,
        "education_type": SPECIALIST,
        "is_hidden": False,
    },
    {
        "username": "smirnova",
        "full_name": "Мария Смирнова",
        "email": "smirnova@gmail.com",
        "phone_number": "89263471805",
        "bio": "Занимаюсь научными проектами.",
        "course": 4,
        "faculty": ISHNKB,
        "education_type": PHD,
        "is_hidden": False,
    },
    {
        "username": "volkov",
        "full_name": "Алексей Волков",
        "email": "volkov@gmail.com",
        "phone_number": "+79851234076",
        "bio": "Интересуюсь базами данных.",
        "course": 3,
        "faculty": ISHITR,
        "education_type": BACHELOR,
        "is_hidden": False,
    },
    {
        "username": "orlova",
        "full_name": "Ольга Орлова",
        "email": "orlova@mail.ru",
        "phone_number": "+79999999999",
        "bio": "Изучаю иностранные языки.",
        "course": 1,
        "faculty": ISHNPT,
        "education_type": MASTER,
        "is_hidden": False,
    },
    {
        "username": "fedorov",
        "full_name": "Дмитрий Федоров",
        "email": "fedorov@mail.ru",
        "phone_number": "89764523108",
        "bio": "Участвую в спортивных соревнованиях.",
        "course": 5,
        "faculty": ISHHBMT,
        "education_type": SPECIALIST,
        "is_hidden": False,
    },
    {
        "username": "nikitina",
        "full_name": "Елена Никитина",
        "email": "nikitina@mail.ru",
        "phone_number": "88888888888",
        "bio": "Люблю работать с большими данными.",
        "course": 3,
        "faculty": ISHB,
        "education_type": BACHELOR,
        "is_hidden": False,
    },
    {
        "username": "morozov",
        "full_name": "Илья Морозов",
        "email": "morozov@mail.ru",
        "phone_number": "+79641237805",
        "bio": "Разрабатываю учебные приложения.",
        "course": 2,
        "faculty": PISHIES,
        "education_type": MASTER,
        "is_hidden": True,
    },
    {
        "username": "kuznetsova",
        "full_name": "Софья Кузнецова",
        "email": "kuznetsova@mail.ru",
        "phone_number": "+78162345097",
        "bio": "Интересуюсь компьютерной графикой.",
        "course": 4,
        "faculty": YUTI,
        "education_type": PHD,
        "is_hidden": True,
    },
]


def main() -> None:
    init_db()
    random.seed(42)

    with Session(engine) as session:
        for data in USERS:
            username = data["username"]
            session.add(
                User(
                    **data,
                    photo_url=None,
                    rating=random.randint(0, 100),
                    is_admin=False,
                    hashed_password=get_password_hash(username.title() + "1!@"),
                )
            )

        session.add(
            User(
                username="admin",
                full_name="Администратор",
                email="admin@admin.admin",
                phone_number="+77031234567",
                bio="Администратор системы.",
                course=1,
                faculty=ISHITR,
                education_type=MASTER,
                is_hidden=True,
                is_admin=True,
                hashed_password=get_password_hash("Admin1!@"),
            )
        )
        session.commit()


if __name__ == "__main__":
    main()
