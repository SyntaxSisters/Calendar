from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column

Base = declarative_base()

db_url = "sqlite:///my_database.db"
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Association tables
User_Group = Table(
    'User_Group', Base.metadata,
    Column('user_id', Integer, ForeignKey('User.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('Group.id'), primary_key=True)
)

Group_Event = Table(
    'Group_Event', Base.metadata,
    Column('event_id', Integer, ForeignKey('Event.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('Group.id'), primary_key=True)
)

User_Event = Table(
    'User_Event', Base.metadata,
    Column('event_id', Integer, ForeignKey('Event.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('User.id'), primary_key=True)
)

#base tables
class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(64))
    groups: Mapped[list['Group']] = relationship(secondary=User_Group, back_populates='users')
    events: Mapped[list['Event']] = relationship(secondary=User_Event, back_populates='users')

class Group(Base):
    __tablename__ = 'Group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32))
    users: Mapped[list['User']] = relationship(secondary=User_Group, back_populates='groups')
    events: Mapped[list['Event']] = relationship(secondary=Group_Event, back_populates='groups')

class Event(Base):
    __tablename__ = 'Event'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beginning: Mapped[DateTime] = mapped_column(DateTime)
    ending: Mapped[DateTime] = mapped_column(DateTime)
    title: Mapped[str] = mapped_column(String(100))
    descr: Mapped[str] = mapped_column(String(500))
    place: Mapped[str] = mapped_column(String(100))
    groups: Mapped[list['Group']] = relationship(secondary=Group_Event, back_populates='events')
    users: Mapped[list['User']] = relationship(secondary=User_Event, back_populates='events')

# Create tables (so you can actually use it :3)
Base.metadata.create_all(engine)
