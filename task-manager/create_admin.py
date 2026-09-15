from sqlmodel import select
from app.database import engine, Session
from app.models import User
from app.enums import Role
from app.security import hash_password


def create_admin_user():
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == "admin")).first()
        if existing:
            print("Admin user already exists!")
            return

        admin_user = User(
            username="admin",
            email="admin@admin.com",
            hashed_password=hash_password("admin123"),
            role=Role.admin
        )
        session.add(admin_user)
        session.commit()
        print("Admin user created successfully! (Username: admin, Password: admin123)")


if __name__ == "__main__":
    create_admin_user()