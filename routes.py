import sys
from flask import *
import random, string
from database_functions import *
from datetime import datetime

app = Flask(__name__)
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


@app.route('/')
def _showIndex():
    return render_template('index.html')


@app.route('/students', methods=['GET', 'POST'])
def _showStudents():
    if request.method == 'POST':
        name = request.form.get('search')
        student = getStudentByName(name)
        if student:
            return render_template('allstudents.html', students=student)
        else:
            flash('Student name is not in our database')
            students = getAllStudents()
            render_template('allstudents.html', students=students)

    students = getAllStudents()
    return render_template('allstudents.html', students=students)

@app.route('/students/<int:studentId>')
def _studentDetails(studentId):
    student = getStudentById(studentId)
    grades = getStudentGrades(studentId)
    notes = getStudentNotes(studentId)
    payments = getStudentPayments(studentId)
    return render_template('student.html', student=student, notes=notes, grades=grades, payments=payments)


@app.route('/students/new', methods=['GET', 'POST'])
def _newStudent():
    fathers = getAllFathers()
    mothers = getAllMothers()
    if request.method == 'GET':
        return render_template('newstudent.html', fathers=fathers, mothers=mothers)
    else :
        if request.form['submit'] == 'save':
            name = request.form.get('name')
            mobile = request.form.get('mobile')
            email = request.form.get('email')
            notes = request.form.get('notes')
            father = request.form.get('father')
            mother = request.form.get('mother')
            # check for father and mother in database
            if not checkParent(father):
                flash("father is not in our database, please add his info")
                return render_template('newstudent.html', name=name,
                    mobile=mobile,
                    email=email,
                    notes=notes,
                    mother=mother)

            if not checkParent(mother):
                flash("mother is not in our database, please add her info")
                return render_template('newstudent.html', name=name,
                    mobile=mobile,
                    email=email,
                    notes=notes,
                    father=father)

            addNewStudent(name, mobile, email, notes, father, mother)
            flash("Student added")
            return redirect(url_for('_showIndex'))
        else:
            return redirect(url_for('_showIndex'))



@app.route('/students/<int:studentId>/edit', methods=['GET', 'POST'])
def _editStudent(studentId):
    student = getStudentById(studentId)
    print(student)
    if request.method == 'GET':
        return render_template('editstudent.html', student=student)
    else:
        if request.form['submit'] == 'save':
            name = request.form.get('name')
            mobile = request.form.get('mobile')
            email = request.form.get('email')
            notes = request.form.get('notes')
            father = request.form.get('father')
            mother = request.form.get('mother')
            # check for father and mother in database
            if not checkParent(father):
                flash("father is not in our database, please add his info")
                return render_template('editstudent.html', student=student)

            if not checkParent(mother):
                flash("mother is not in our database, please add her info")
                return render_template('editstudent.html', student=student)

            editStudent(student.id, name, mobile, email, notes, father, mother)
            flash('Student Information Updated')
            students = getAllStudents()
            return render_template('allstudents.html', students=students)
        else:
            return redirect(url_for('_showIndex'))


@app.route('/students/<int:studentId>/delete', methods=['GET', 'POST'])
def _deleteStudent(studentId):
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('deletestudent.html', student=student)
    else:
        if request.form['submit'] == 'delete':
            deleteStudentGrades(studentId)
            deleteStudentNotes(studentId)
            deleteStudentPayments(studentId)
            deleteStudent(studentId)
            flash('All Student Data deleted')
            students = getAllStudents()
            return redirect(url_for('_showStudents',students=students))
        else:
            return redirect(url_for('_showIndex'))


@app.route('/students/<int:studentId>/grades')
def _showStudentGrades(studentId):
    return "Student ID " + str(studentId) + " Grades"


@app.route('/students/<int:studentId>/grades/new', methods=['GET', 'POST'])
def _addStudentGrades(studentId):
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('newgrade.html', student=student)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            grade = request.form.get('grade')
            notes = request.form.get('notes')
            newGrade = Grades(student_id= studentId,
                              grade= grade,
                              date= valdate,
                              notes= notes)
            session.add(newGrade)
            session.commit()
            flash('Student Grade Saved')
            return redirect(url_for('_studentDetails',studentId= studentId))


@app.route('/students/<int:studentId>/grades/<int:gradesId>/edit', methods=['GET', 'POST'])
def _editStudentGrades(studentId, gradesId):
    if request.method == 'GET':
        return " Edit grade ID " + str(gradesId) + " for Student ID " + str(studentId)
    else:
        return "Do Edit grade ID " + str(gradesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/grades/<int:gradesId>/delete', methods=['GET', 'POST'])
def _deleteStudentGrades(studentId, gradesId):
    if request.method == 'GET':
        return "Are you sure to delete grade ID " + str(gradesId) + " for Student ID " + str(studentId)
    else:
        return "Do delete grade ID " + str(gradesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/notes')
def _showStudentNotes(studentId):
    return "Student ID " + str(studentId) + " Notes"


@app.route('/students/<int:studentId>/notes/new', methods=['GET', 'POST'])
def _addStudentNotes(studentId):
    if request.method == 'GET':
        return " Add note for Student ID " + str(studentId)
    else:
        return "Do Add note for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/notes/<int:notesId>/edit', methods=['GET', 'POST'])
def _editStudentNotes(studentId, notesId):
    if request.method == 'GET':
        return " Edit note ID " + str(notesId) + " for Student ID " + str(studentId)
    else:
        return "Do Edit note ID " + str(notesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/notes/<int:notesId>/delete', methods=['GET', 'POST'])
def _deleteStudentNotes(studentId, notesId):
    if request.method == 'GET':
        return "Are you sure to delete note ID " + str(notesId) + " for Student ID " + str(studentId)
    else:
        return "Do delete note ID " + str(notesId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/payments')
def _showStudentPayments(studentId):
    return "Student ID " + str(studentId) + " Payments"


@app.route('/students/<int:studentId>/payments/new', methods=['GET', 'POST'])
def _addStudentPayments(studentId):
    if request.method == 'GET':
        return " Add payment for Student ID " + str(studentId)
    else:
        return "Do Add payment for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/payments/<int:paymentsId>/edit', methods=['GET', 'POST'])
def _editStudentPayments(studentId, paymentsId):
    if request.method == 'GET':
        return " Edit payment ID " + str(paymentsId) + " for Student ID " + str(studentId)
    else:
        return "Do Edit payment ID " + str(paymentsId) + " for Student ID " + str(studentId)


@app.route('/students/<int:studentId>/payments/<int:paymentsId>/delete', methods=['GET', 'POST'])
def _deleteStudentPayments(studentId, paymentsId):
    if request.method == 'GET':
        return "Are you sure to delete payment ID " + str(paymentsId) + " for Student ID " + str(studentId)
    else:
        return "Do delete payment ID " + str(paymentsId) + " for Student ID " + str(studentId)


@app.route('/parents/new', methods=['GET', 'POST'])
def _newParent():
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
            addNewParent(name=name, sex=sex, mobile=mobile, address=address, job=job, email=email, notes=notes)
            flash('Parent Added Successfully')
            return redirect(url_for('_showIndex'))
        else :
            return redirect(url_for('_showIndex'))


@app.route('/parents')
def _showAllParents():
    parents = getAllParents()
    return render_template('allparents.html', parents = parents)

@app.route('/cv')
def _getCV():
    return render_template('cv.html')


@app.route('/fathers/json')
def getFathersJson():
    fathers = getAllFathers()
    return jsonify([father.serialize for father in fathers])


@app.route('/mothers/json')
def getMothersJson():
    mothers = getAllMothers()
    return jsonify([mother.serialize for mother in mothers])


@app.route('/students/json')
def getStudentsJson():
    students = getAllStudents()
    return jsonify([student.serialize for student in students])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = secret_key
    app.run(host='0.0.0.0', port='5000')