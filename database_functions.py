from config import Config
#from sqlalchemy import *
from routes import current_user, db
from models import Users, Parents, Notes, Payments, Grades, Students, Courses





#engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,
#                      connect_args={'check_same_thread': False})
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
session = db.session()


def addNewStudent(name, mobile, email, notes, father, mother):
    newStudent = Students(name = name,
            mobile = mobile,
            email = email,
            notes = notes,
            father = father,
            mother = mother)
    session.add(newStudent)
    session.flush()
    if father:
        f = session.query(Parents).filter_by(name=father).first()
        f.students.append(newStudent)
        session.add(f)
    if mother:
        m = session.query(Parents).filter_by(name=mother).first()
        m.students.append(newStudent)
        session.add(m)
    session.commit()


def editStudent(id, name, mobile, email, notes, father, mother):
    student = getStudentById(id)
    if father != student.father or mother != student.mother:
        newFather = session.query(Parents).filter_by(name=father).first()
        newMother = session.query(Parents).filter_by(name=mother).first()
        student.parents = []
        session.commit()
        if newFather:
            student.parents.append(newFather)
        if newMother:
            student.parents.append(newMother)

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
    result = session.query(Users).filter_by(username=username).first()
    if result:
        return False
    else:
        return True


def checkEditUsernameAvailable(id, username):
    result = session.query(Users).filter(and_(Users.username == username, Users.id != id)).first()
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
                notes = notes)
    session.add(newParent)
    session.flush()
    if username:
        newUser = Users(username=username,
            parent_id=newParent.id)
        newUser.set_password(password)
        session.add(newUser)
    session.commit()


def getAllParents():
    if current_user.admin == 1:
        return session.query(Parents).all()
    else:
        return session.query(Parents).filter_by(id = current_user.parent_id).all()


def getAllFathers():
    return session.query(Parents).filter_by(sex = 'Male').all()


def getAllMothers():
    return session.query(Parents).filter_by(sex = 'Female').all()


def getAllStudents():
    if current_user.admin != 1:
        # return session.query(Students).filter(or_(Students.father == current_user.name, Students.mother == current_user.name))
        return session.query(Parents).filter_by(id = current_user.parent_id).first().students
    return session.query(Students).all()


def checkParent(parentName):
    parent = session.query(Parents).filter_by(name=parentName).first()
    if parent is None:
        return False
    else:
        return True


def getStudentByName(name):
    if current_user.admin != 1:
        return session.query(Parents).filter_by(id = current_user.parent_id).first().students
        #return session.query(Students).filter(and_(Students.name == name , or_(Students.father == current_user.name, Students.mother == current_user.name)))
    return session.query(Students).filter_by(name=name).first()



def getParentByName(name):
    return session.query(Parents).filter_by(name=name).all()


def getUserByUsername(username):
    user = session.query(Users).filter_by(username=username).first()
    return user


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
    student = session.query(Students).filter_by(id=studentId).one()
    student.parents = []
    session.delete(student)
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
    #return session.query(Students).filter(or_(Students.father==parentName, Students.mother==parentName)).all()
    parent = session.query(Parents).filter_by(name = parentName).first()
    return parent.students


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


def addGrade(studentId, grade, valdate, notes):
    newGrade = Grades(student_id=studentId,
                      grade=grade,
                      date=valdate,
                      notes=notes)
    session.add(newGrade)
    session.commit()

def editGrade(grade, studentId, ggrade, valdate, notes):
    grade.student_id = studentId
    grade.grade = ggrade
    grade.date = valdate
    grade.notes = notes
    session.add(grade)
    session.commit()


def addNote(studentId, note, valdate, notes):
    newNote = Notes(student_id=studentId,
                    note=note,
                    date=valdate,
                    notes=notes)
    session.add(newNote)
    session.commit()


def editNote(note, studentId, nnote, valdate, notes):
    note.student_id = studentId
    note.grade = nnote
    note.date = valdate
    note.notes = notes
    session.add(note)
    session.commit()


def addPayment(studentId, payment, valdate, notes):
    newPayment = Payments(student_id=studentId,
                          payment=payment,
                          date=valdate,
                          notes=notes)
    session.add(newPayment)
    session.commit()


def editPayment(payment, studentId, ppayment, valdate, notes):
    payment.student_id = studentId
    payment.payment = ppayment
    payment.date = valdate
    payment.notes = notes
    session.add(payment)
    session.commit()


def editUsername(userId, newUsername):
    user = session.query(Users).filter_by(id=userId).first()
    user.username = newUsername
    session.add(user)
    session.commit()


def editPassword(userId, newPassword):
    user = session.query(Users).filter_by(id=userId).first()
    user.set_password(newPassword)
    session.add(user)
    session.commit()


def insertAdminUser():
    user = Users(username='admin', admin=1)
    user.set_password('123654')

    admin = session.query(Users).filter_by(username='admin').first()
    if not admin:
        session.add(user)
        session.commit()


def addCourse(name, notes):
    course = Courses(name=name, notes=notes)
    session.add(course)
    session.commit()


def getAllCourses():
    return session.query(Courses).all()

def getCourseById(id):
    return session.query(Courses).filter_by(id=id).first()

def editCourse(course):
    session.add(course)
    session.commit()