from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from ingameleader.model.side import Side

Base = declarative_base()


class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    map_id = Column(Integer, ForeignKey("map.id"), nullable=False)
    map = relationship("Map")
    exemplar_routes = relationship("ExemplarRoute", backref="strategy")

    name = Column(String, unique=False)

    alpha = Column(Integer, nullable=False)
    beta = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    side = Column(Enum(Side), nullable=False)

    def __str__(self):
        return f"Strategy(name={self.name}, wins={self.losses}, wins={self.wins}, side={self.side})"


class Map(Base):
    __tablename__ = "map"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    strategies = relationship("Strategy")
    locations = relationship("Location", backref="map")

    name = Column(String, unique=True)
    ugly_name = Column(String, unique=True)

    def __str__(self):
        return f"Map(name={self.name})"

    def __repr__(self):
        return str(self)


class ExemplarRoute(Base):
    __tablename__ = "exemplar_route"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    strategy_id = Column(Integer, ForeignKey("strategy.id"), nullable=False)
    route_to_locations = relationship("RouteToLocation")


class RouteToLocation(Base):
    __tablename__ = "route_to_location"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    route_id = Column(Integer, ForeignKey("exemplar_route.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    location = relationship("Location", uselist=False)


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    map_id = Column(Integer, ForeignKey("map.id"), nullable=False)

    name = Column(String, unique=False, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    def __str__(self):
        return f"Location(name={self.name}, x={self.x}, y={self.y})"

    def __repr__(self):
        return str(self)


@contextmanager
def create_session():
    engine = create_engine("sqlite:///db.db")
    yield sessionmaker(bind=engine)()
