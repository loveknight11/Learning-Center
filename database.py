from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from passlib.apps import custom_app_context as pwd_context
import random
import string

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class Students(Base):
	__tablename__ = 'students'
	id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = Column(String)
    email = Column(String)
    notes = Column(String)
    father_id = Column(Integer, ForeignKey('parents.id'))
    mother_id = Column(Integer, ForeignKey('parents.id'))


class Parents(Base):
	__tablename__ = 'parents'
	id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = Column(String)
    address = Column(String)
    job = Column(String)
    email = Column(String)
    notes = Column(String)



class Grades(Base):
	__tablename__ = 'grades'
	id = Column(Integer, primary_key=True)
	student_id = Column(Integer, ForeignKey('students.id'))
	grade = Column(String)
	date = Column(DateTime, default=func.now())
	notes = Column(String)