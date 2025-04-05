from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Table, Column, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column

Base = declarative_base()

db_url = "sqlite:///my_database.db"
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Association tables (only needed for Event-Group and Event-User relationships)
Group_Event = Table(
    'Group_Event', Base.metadata,
    Column('event_id', String, ForeignKey('Event.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('Group.id'), primary_key=True)
)

User_Event = Table(
    'User_Event', Base.metadata,
    Column('event_id', String, ForeignKey('Event.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('User.id'), primary_key=True)
)

#base tables
class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(64))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('Group.id'))  # One-to-many relation
    group: Mapped['Group'] = relationship('Group', back_populates='users')
    events: Mapped[list['Event']] = relationship(secondary=User_Event, back_populates='users')

class Group(Base):
    __tablename__ = 'Group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(32))
    users: Mapped[list['User']] = relationship('User', back_populates='group')
    events: Mapped[list['Event']] = relationship(secondary=Group_Event, back_populates='groups')

class Event(Base):
    __tablename__ = 'Event'
    id: Mapped[str] = mapped_column(String, primary_key=True)
    start_date: Mapped[Date] = mapped_column(Date)  # Now only stores the date
    start_time: Mapped[Time] = mapped_column(Time)
    end_time: Mapped[Time] = mapped_column(Time)
    tags: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(7))
    team_name: Mapped[str] = mapped_column(String(50))
    attachments: Mapped[str] = mapped_column(String(500))
    pdf_summary: Mapped[str] = mapped_column(String(500))
    groups: Mapped[list['Group']] = relationship(secondary=Group_Event, back_populates='events')
    users: Mapped[list['User']] = relationship(secondary=User_Event, back_populates='events')

# Create tables (so you can actually use it :3)
Base.metadata.create_all(engine)
