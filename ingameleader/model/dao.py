from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ingameleader.model.side import Side

Base = declarative_base()


class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    map_id = Column(Integer, ForeignKey("map.id"), nullable=False)

    name = Column(String, unique=True)

    alpha = Column(Integer, nullable=False)
    beta = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    side = Column(Enum(Side), nullable=False)


class Map(Base):
    __tablename__ = "map"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    strategies = relationship("Strategy", backref="player")

    name = Column(String, unique=True)


from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


@contextmanager
def create_session():
    engine = create_engine("sqlite:///db.db")
    yield sessionmaker(bind=engine)()
