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
		return "Edit Student ID " + studentId
	else:
		return "Do Edit Student ID " + studentId


@app.route('/students/<int:studentId>/delete', methods=['GET', 'POST'])
def deleteStudent(studentId):
	if request.method == 'GET':
		return "Are you sure to delete Student ID " + studentId
	else:
		return "Do delete Student ID " + studentId


@app.route('/students/<int:studentId>/grades')
def showStudentGrades(studentId):
	return "Student ID " + studentId + " Grades"


@app.route('/students/<int:studentId>/grades/new', methods=['GET', 'POST'])
def addStudentGrades(studentId):
	if request.method == 'GET':
		return " Add grade for Student ID " + studentId
	else:
		return "Do Add grade for Student ID " + studentId


@app.route('/students/<int:studentId>/grades/<int:gradesId>/edit', methods=['GET', 'POST'])
def editStudentGrades(studentId, gradesId):
	if request.method == 'GET':
		return " Edit grade ID " + gradesId + " for Student ID " + studentId
	else:
		return "Do Edit grade ID " + gradesId + " for Student ID " + studentId


@app.route('/students/<int:studentId>/grades/<int:gradesId>/delete', methods=['GET', 'POST'])
def deleteStudentGrades(studentId, gradesId):
	if request.method == 'GET':
		return "Are you sure to delete grade ID " + gradesId + " for Student ID " + studentId
	else:
		return "Do delete grade ID " + gradesId + " for Student ID " + studentId


@app.route('/students/<int:studentId>/notes')
def showStudentNotes(studentId):
	return "Student ID " + studentId + " Notes"


@app.route('/students/<int:studentId>/notes/new', methods=['GET', 'POST'])
def addStudentNotes(studentId):
	if request.method == 'GET':
		return " Add note for Student ID " + studentId
	else:
		return "Do Add note for Student ID " + studentId


@app.route('/students/<int:studentId>/notes/<int:notesId>/edit', methods=['GET', 'POST'])
def editStudentNotes(studentId, notesId):
	if request.method == 'GET':
		return " Edit note ID " + notesId + " for Student ID " + studentId
	else:
		return "Do Edit note ID " + notesId + " for Student ID " + studentId


@app.route('/students/<int:studentId>/notes/<int:notesId>/delete', methods=['GET', 'POST'])
def deleteStudentNotes(studentId, notesId):
	if request.method == 'GET':
		return "Are you sure to delete note ID " + notesId + " for Student ID " + studentId
	else:
		return "Do delete note ID " + notesId + " for Student ID " + studentId


@app.route('/students/<int:studentId>/payments')
def showStudentPayments(studentId):
	return "Student ID " + studentId + " Payments"


@app.route('/students/<int:studentId>/payments/new', methods=['GET', 'POST'])
def addStudentPayments(studentId):
	if request.method == 'GET':
		return " Add payment for Student ID " + studentId
	else:
		return "Do Add payment for Student ID " + studentId


@app.route('/students/<int:studentId>/payments/<int:paymentsId>/edit', methods=['GET', 'POST'])
def editStudentPayments(studentId, paymentsId):
	if request.method == 'GET':
		return " Edit payment ID " + paymentsId + " for Student ID " + studentId
	else:
		return "Do Edit payment ID " + paymentsId + " for Student ID " + studentId


@app.route('/students/<int:studentId>/payments/<int:paymentsId>/delete', methods=['GET', 'POST'])
def deleteStudentPayments(studentId, paymentsId):
	if request.method == 'GET':
		return "Are you sure to delete payment ID " + paymentsId + " for Student ID " + studentId
	else:
		return "Do delete payment ID " + paymentsId + " for Student ID " + studentId


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port='5000')