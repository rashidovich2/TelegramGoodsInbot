from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"



class Artist(Base):
    __tablename__ = "storage_artists"

    increment = Column(Integer, primary_key=True)
    artist_id = Column(Integer)
    name = Column(String(50))
    description = Column(String)
    webaddress = Column(String)
    admin = Column(Integer)
    logo = Column(String)
    paymdir = Column(String)
    city = Column(String)
    geocode = Column(String)
    city_id = Column(Integer)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Artist(id={self.id!r}, name={self.name!r}, admin={self.admin!r})"

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
