import bcrypt
from sqlalchemy import Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    uname: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    _password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    
    name: Mapped[str] = mapped_column(String(15))
    sub_name: Mapped[str] = mapped_column(String(50))
    sur_name: Mapped[str] = mapped_column(String(50))

    yo: Mapped[int] = mapped_column(Integer)
    mass: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    
    desc: Mapped[str | None] = mapped_column(String(200))

    @hybrid_property
    def password(self) -> str:
        raise AttributeError("Пароль не предназначен для чтения!")

    @password.setter
    def password(self, plain_password: str) -> None:
        password_bytes = plain_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        self._password_hash = hashed.decode('utf-8')

    def check_password(self, plain_password: str) -> bool:
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = self._password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)