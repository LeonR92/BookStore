from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from core.models import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(250), nullable=False, default="Unknown")
    last_name = Column(String(250), nullable=False, default="Unknown")
    dob = Column(DateTime, nullable=True)
    country = Column(String(150), nullable=True)

    # Foreign Keys
    credentials_id = Column(Integer, ForeignKey("credentials.id", ondelete="CASCADE"), nullable=False, unique=True)
    mfa_id = Column(Integer, ForeignKey("mfa.id", ondelete="SET NULL"), nullable=True, unique=True)

    # Relationships
    credentials = relationship("Credentials", back_populates="user", uselist=False, cascade="all, delete")
    mfa = relationship("MFA", back_populates="user", uselist=False, cascade="all, delete")



class Credentials(Base, TimestampMixin):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(320), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)  
    last_login = Column(DateTime, nullable=True)

    # Relationship
    user = relationship("User", back_populates="credentials", uselist=False)


class MFA(Base, TimestampMixin):
    __tablename__ = "mfa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    totp_secret = Column(String(100), nullable=True) 

    # Relationship
    user = relationship("User", back_populates="mfa", uselist=False)

