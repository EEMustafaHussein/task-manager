from sqlmodel import create_engine, Session
from app.config import settings

# تهيئة محرك قاعدة البيانات
connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, connect_args=connect_args)

# دالة تجهيز جلسة الاتصال لتستخدم في المسارات
def get_session():
    with Session(engine) as session:
        yield session