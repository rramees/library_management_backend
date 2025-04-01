from sqlalchemy import Column, Integer, String, Enum
from app.db import Base
import enum

class UserRole(enum.Enum):
    LIBRARIAN = "librarian"
    USER = "user"

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_no = Column(String(20), unique=True)
    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=UserRole.USER)
    api_key = Column(String(255), unique=True, index=True)
    status = Column(Enum(UserStatus, values_callable=lambda obj: [e.value for e in obj]), default=UserStatus.ACTIVE)
