from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from passlib.apps import custom_app_context as pwd_context
import random
import string
import datetime

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = Column(String)
    email = Column(String)
    notes = Column(String)
    father = Column(Integer, ForeignKey('parents.name'))
    mother = Column(Integer, ForeignKey('parents.name'))


class Parents(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = Column(String)
    address = Column(String)
    job = Column(String)
    email = Column(String)
    notes = Column(String)
    sex = Column(String)


    @property
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'mobile': self.mobile,
                'address': self.address,
                'job': self.job,
                'email': self.email,
                'notes': self.notes,
                'sex': self.sex
        }

class Grades(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    grade = Column(String)
    date = Column(DateTime, default=datetime.datetime.now)
    notes = Column(String)


class Notes(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    note = Column(String)
    date = Column(DateTime, default=datetime.datetime.now)
    notes = Column(String)


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    payment = Column(String)
    date = Column(DateTime, default=datetime.datetime.now)
    notes = Column(String)


engine = create_engine('sqlite:///db.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.create_all(engine)