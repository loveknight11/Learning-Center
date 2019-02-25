from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from passlib.apps import custom_app_context as pwd_context
import random
import string
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from routes import login, db



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

    @property
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'mobile': self.mobile,
                'email': self.email,
                'notes': self.notes,
                'father': self.father,
                'mother': self.mother
        }


class Parents(UserMixin, db.Model, Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = Column(String)
    address = Column(String)
    job = Column(String)
    email = Column(String)
    notes = Column(String)
    sex = Column(String)
    username = Column(String)
    password_hash = Column(String)
    admin = Column(Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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


    @login.user_loader
    def load_user(id):
        return Parents.query.get(int(id))



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