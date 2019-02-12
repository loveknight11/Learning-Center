import sys
from flask import *
from sqlalchemy import *
from database import Base, Students, Parents, Grades, Notes, Payments
from sqlalchemy.orm import sessionmaker
import random, string

app = Flask(__name__)
engine = create_engine('sqlite:///db.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


@app.route('/')
def showIndex():
	return render_template('index.html')


@app.route('/students')
def showStudents():
	students = session.query(Students).all()
	return render_template('allstudents.html', students=students)


@app.route('/students/new', methods=['GET', 'POST'])
def newStudent():
	fathers = session.query(Parents).filter_by(sex='Male').all()
	mothers = session.query(Parents).filter_by(sex='Female').all()
	if request.method == 'GET':
		return render_template('newstudent.html', fathers=fathers, mothers=mothers)
	else :
		name = request.form.get('name')
		mobile = request.form.get('mobile')
		email = request.form.get('email')
		notes = request.form.get('notes')
		father = request.form.get('father')
		mother = request.form.get('mother')
		# check for father and mother in database
		chk = False
		for f in fathers:
			if f.name == father:
				chk = True
		if not chk:
			flash("father is not in our database, please add his info")
			return render_template('newstudent.html', name=name,
				mobile=mobile,
				email=email,
				notes=notes,
				mother=mother)

		chk = False
		for m in mothers:
			if m.name == mother:
				chk = True
		if not chk:
			flash("mother is not in our database, please add her info")
			return render_template('newstudent.html', name=name,
				mobile=mobile,
				email=email,
				notes=notes,
				father=father)

		newStudent = Students(name = name,
			mobile = mobile,
			email = email,
			notes = notes,
			father = father,
			mother = mother)
		session.add(newStudent)
		session.commit()
		flash("Student added")
		return redirect(url_for('showIndex'))



@app.route('/students/<int:studentId>/edit', methods=['GET', 'POST'])
def editStudent(studentId):
	if request.method == 'GET':
		return "Edit Student ID " + str(studentId)
	else:
		return "Do Edit Student ID " + str(studentId)


@app.route('/students/<int:studentId>/delete', methods=['GET', 'POST'])
def deleteStudent(studentId):
	if request.method == 'GET':
		return "Are you sure to delete Student ID " + str(studentId)
	else:
		return "Do delete Student ID " + str(studentId)


@app.route('/students/<int:studentId>/grades')
def showStudentGrades(studentId):
	return "Student ID " + str(studentId) + " Grades"


@app.route('/students/<int:studentId>/grades/new', methods=['GET', 'POST'])
def addStudentGrades(studentId):
	if request.method == 'GET':
		return " Add grade for Student ID " + str(studentId)
	else:
		return "Do Add grade for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/grades/<int:gradesId>/edit', methods=['GET', 'POST'])
def editStudentGrades(studentId, gradesId):
	if request.method == 'GET':
		return " Edit grade ID " + str(gradesId) + " for Student ID " + str(studentId)
	else:
		return "Do Edit grade ID " + str(gradesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/grades/<int:gradesId>/delete', methods=['GET', 'POST'])
def deleteStudentGrades(studentId, gradesId):
	if request.method == 'GET':
		return "Are you sure to delete grade ID " + str(gradesId) + " for Student ID " + str(studentId)
	else:
		return "Do delete grade ID " + str(gradesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/notes')
def showStudentNotes(studentId):
	return "Student ID " + str(studentId) + " Notes"


@app.route('/students/<int:studentId>/notes/new', methods=['GET', 'POST'])
def addStudentNotes(studentId):
	if request.method == 'GET':
		return " Add note for Student ID " + str(studentId)
	else:
		return "Do Add note for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/notes/<int:notesId>/edit', methods=['GET', 'POST'])
def editStudentNotes(studentId, notesId):
	if request.method == 'GET':
		return " Edit note ID " + str(notesId) + " for Student ID " + str(studentId)
	else:
		return "Do Edit note ID " + str(notesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/notes/<int:notesId>/delete', methods=['GET', 'POST'])
def deleteStudentNotes(studentId, notesId):
	if request.method == 'GET':
		return "Are you sure to delete note ID " + str(notesId) + " for Student ID " + str(studentId)
	else:
		return "Do delete note ID " + str(notesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/payments')
def showStudentPayments(studentId):
	return "Student ID " + str(studentId) + " Payments"


@app.route('/students/<int:studentId>/payments/new', methods=['GET', 'POST'])
def addStudentPayments(studentId):
	if request.method == 'GET':
		return " Add payment for Student ID " + str(studentId)
	else:
		return "Do Add payment for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/payments/<int:paymentsId>/edit', methods=['GET', 'POST'])
def editStudentPayments(studentId, paymentsId):
	if request.method == 'GET':
		return " Edit payment ID " + str(paymentsId) + " for Student ID " + str(studentId)
	else:
		return "Do Edit payment ID " + str(paymentsId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/payments/<int:paymentsId>/delete', methods=['GET', 'POST'])
def deleteStudentPayments(studentId, paymentsId):
	if request.method == 'GET':
		return "Are you sure to delete payment ID " + str(paymentsId) + " for Student ID " + str(studentId)
	else:
		return "Do delete payment ID " + str(paymentsId) + " for Student ID " + str(studentId)


@app.route('/parents/new', methods=['GET', 'POST'])
def newParent():
	if request.method == 'GET':
		return render_template('newparent.html')
	else :
		if request.form['submit'] == 'save':
			name = request.form.get('name')
			sex = request.form.get('sex')
			mobile = request.form.get('mobile')
			address = request.form.get('address')
			job = request.form.get('job')
			email = request.form.get('email')
			notes = request.form.get('notes')
			newParent = Parents(name = name,
				sex = sex,
				mobile = mobile,
				address = address,
				job = job,
				email = email,
				notes = notes)
			session.add(newParent)
			session.commit()
			flash('Parent Added Successfully')
			return redirect(url_for('showIndex'))
		else :
			return redirect(url_for('showIndex'))


@app.route('/parents')
def showAllParents():
	parents = session.query(Parents).all()
	return render_template('allparents.html', parents = parents)

@app.route('/cv')
def getCV():
	return render_template('cv.html')


@app.route('/fathers/json')
def getFathersJson():
	fathers = session.query(Parents).filter_by(sex='Male').all()
	return jsonify([father.serialize for father in fathers])


if __name__ == '__main__':
	app.debug = True
	app.secret_key = secret_key
	app.run(host='0.0.0.0', port='5000')