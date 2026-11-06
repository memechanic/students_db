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
        "email": None,
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
        "email": None,
        "phone_number": None,
        "bio": "Увлекаюсь робототехникой.",
        "course": 6,
        "faculty": None,
        "education_type": SPECIALIST,
        "is_hidden": False,
    },
    {
        "username": "smirnova",
        "full_name": "Мария Смирнова",
        "email": None,
        "phone_number": None,
        "bio": "Занимаюсь научными проектами.",
        "course": None,
        "faculty": None,
        "education_type": PHD,
        "is_hidden": False,
    },
    {
        "username": "volkov",
        "full_name": "Алексей Волков",
        "email": None,
        "phone_number": None,
        "bio": "Интересуюсь базами данных.",
        "course": None,
        "faculty": None,
        "education_type": None,
        "is_hidden": False,
    },
    {
        "username": "orlova",
        "full_name": "Ольга Орлова",
        "email": None,
        "phone_number": None,
        "bio": "Изучаю иностранные языки и практикую разговорную речь каждый день.",
        "course": 1,
        "faculty": None,
        "education_type": None,
        "is_hidden": False,
    },
    {
        "username": "fedorov",
        "full_name": "Дмитрий Федоров",
        "email": None,
        "phone_number": None,
        "bio": "Участвую в спортивных соревнованиях и тренируюсь несколько раз в неделю.",
        "course": None,
        "faculty": None,
        "education_type": None,
        "is_hidden": False,
    },
    {
        "username": "nikitina",
        "full_name": "Елена Никитина",
        "email": None,
        "phone_number": None,
        "bio": "Люблю работать с большими данными.",
        "course": None,
        "faculty": None,
        "education_type": None,
        "is_hidden": False,
    },
    {
        "username": "morozov",
        "full_name": "Илья Морозов",
        "email": None,
        "phone_number": None,
        "bio": "Разрабатываю учебные приложения и изучаю новые технологии.",
        "course": None,
        "faculty": None,
        "education_type": None,
        "is_hidden": True,
    },
    {
        "username": "kuznetsova",
        "full_name": "Софья Кузнецова",
        "email": None,
        "phone_number": None,
        "bio": None,
        "course": None,
        "faculty": None,
        "education_type": None,
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
