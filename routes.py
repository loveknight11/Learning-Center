from flask import *

app = Flask(__name__)


@app.route('/')
def showIndex():
	return "you are at index"


@app.route('/students')
def showStudents():
	return "All Students"


@app.route('/students/new', methods=['GET', 'POST'])
def newStudent():
	if request.method == 'GET':
		return "New Student"
	else :
		return "Do New Student"


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


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port='5000')