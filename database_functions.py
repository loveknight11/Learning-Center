from config import Config
from sqlalchemy import *
from database import *
from sqlalchemy.orm import sessionmaker



engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,
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


def editStudent(id, name, mobile, email, notes, father, mother):
    student = getStudentById(id=id)
    student.name = name
    student.mobile = mobile
    student.email = email
    student.notes = notes
    student.father = father
    student.mother = mother
    session.add(student)
    session.commit()


def editParent(id, name, mobile, address, job, email, notes, sex):
    parent = getParentById(id=id)
    parent.name = name
    parent.mobile = mobile
    parent.address = address
    parent.job = job
    parent.email = email
    parent.notes = notes
    parent.sex = sex
    session.add(parent)
    session.commit()


def checkUsernameAvailable(username):
    result = session.query(Parents).filter_by(username=username).first()
    if result:
        return False
    else:
        return True


def checkEditUsernameAvailable(id, username):
    result = session.query(Parents).filter(and_(Parents.username == username, Parents.id != id)).first()
    if result:
        return False
    else:
        return True

def addNewParent(name, sex, mobile, address, job, email, notes, username, password):
    newParent = Parents(name = name,
                sex = sex,
                mobile = mobile,
                address = address,
                job = job,
                email = email,
                notes = notes,
                username=username)
    newParent.set_password(password)
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


def getStudentByName(name):
    student = session.query(Students).filter_by(name=name).first()
    return student


def getParentByName(name):
    return session.query(Parents).filter_by(name=name).all()


def getStudentById(id):
    student = session.query(Students).filter_by(id=id).first()
    return student


def getParentById(id):
    parent = session.query(Parents).filter_by(id=id).first()
    return parent


def deleteStudentGrades(studentId):
    grades = session.query(Grades).filter_by(student_id=studentId).delete()
    session.commit()


def deleteStudentNotes(studentId):
    notes = session.query(Notes).filter_by(student_id=studentId).delete()
    session.commit()


def deleteStudentPayments(studentId):
    payments = session.query(Payments).filter_by(student_id=studentId).delete()
    session.commit()


def deleteStudent(studentId):
    student = session.query(Students).filter_by(id=studentId).delete()
    session.commit()


def getStudentGrades(studentId):
    return session.query(Grades).filter_by(student_id=studentId).all()

def getStudentNotes(studentId):
    return session.query(Notes).filter_by(student_id=studentId).all()

def getStudentPayments(studentId):
    return session.query(Payments).filter_by(student_id=studentId).all()

def getGrade(gradesId):
    return session.query(Grades).filter_by(id=gradesId).first()

def deleteGrade(gradeId):
    session.query(Grades).filter_by(id=gradeId).delete()
    session.commit()

def getNote(notesId):
    return session.query(Notes).filter_by(id=notesId).first()


def deleteNote(notesId):
    session.query(Notes).filter_by(id=notesId).delete()
    session.commit()


def getPayment(paymentsId):
    return session.query(Payments).filter_by(id=paymentsId).first()


def deletePayment(paymentsId):
    session.query(Payments).filter_by(id=paymentsId).delete()
    session.commit()

def getStudentsForParent(parentName):
    return session.query(Students).filter(or_(Students.father==parentName, Students.mother==parentName)).all()


def deleteParent(parentId):
    session.query(Parents).filter_by(id=parentId).delete()
    session.commit()


def editStudentParentName(oldParentName, newParentName):
    studentsForFather = session.query(Students).filter_by(father=oldParentName).all()
    studentsForMother = session.query(Students).filter_by(mother=oldParentName).all()
    for student in studentsForFather:
        student.father = newParentName
    for student in studentsForMother:
        student.mother = newParentName
    session.commit()