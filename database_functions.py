from sqlalchemy import *
from database import Base, Students, Parents, Grades, Notes, Payments
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def addNewStudent(name, mobile, email, notes, father, mother):
	newStudent = Students(name = name,
			mobile = mobile,
			email = email,
			notes = notes,
			father = father,
			mother = mother)
	session.add(newStudent)
	session.commit()


def addNewParent(name, sex, mobile, address, job, email, notes):
	newParent = Parents(name = name,
				sex = sex,
				mobile = mobile,
				address = address,
				job = job,
				email = email,
				notes = notes)
	session.add(newParent)
	session.commit()


def getAllParents():
	return session.query(Parents).all()


def getAllFathers():
	return session.query(Parents).filter_by(sex='Male').all()


def getAllMothers():
	return session.query(Parents).filter_by(sex='Female').all()


def getAllStudents():
	return session.query(Students).all()


def checkParent(parentName):
	parent = session.query(Parents).filter_by(name=parentName).first()
	print(parent)
	if parent is None:
		return False
	else:
		return True