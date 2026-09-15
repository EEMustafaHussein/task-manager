from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session
from app.config import settings
from app.database import get_session
from app.models import User
from app.enums import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(User.select().where(User.username == username)).first() if hasattr(User,
                                                                                           "select") else session.query(
        User).filter(User.username == username).first()
    # لتجنب مشاكل استعلام SQLModel الحديثة، نستخدم الطريقة الأبسط والأضمن:
    user = session.query(User).filter(User.username == username).first() if hasattr(session, "query") else session.exec(
        User.__table__.select().where(User.username == username)).first()

    # الطريقة الأدق والأحدث مع SQLModel:
    from sqlmodel import select
    user = session.exec(select(User).where(User.username == username)).first()

    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_roles(allowed_roles: list[Role]):
    def role_verifier(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user

    return role_verifier