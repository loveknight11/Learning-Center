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
    student = getStudentById(studentId)
    grade = getGrade(gradesId)
    if request.method == 'GET':
        print(grade)
        return render_template('editgrade.html', student=student, grade=grade)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            ggrade = request.form.get('grade')
            notes = request.form.get('notes')
            grade.student_id = studentId
            grade.grade= ggrade
            grade.date= valdate
            grade.notes= notes
            session.add(grade)
            session.commit()
            flash('Student Grade Edited')

        return redirect(url_for('_studentDetails', studentId=studentId))


@app.route('/students/<int:studentId>/grades/<int:gradesId>/delete', methods=['GET', 'POST'])
def _deleteStudentGrades(studentId, gradesId):
    student = getStudentById(studentId)
    grade = getGrade(gradesId)
    if request.method == 'GET':
        return render_template('deletegrade.html', student=student)
    else:
        if request.form['submit'] == 'delete':
            deleteGrade(gradesId)
            flash('grade deleted')

        return redirect(url_for('_studentDetails', studentId=studentId))


@app.route('/students/<int:studentId>/notes')
def _showStudentNotes(studentId):
    return "Student ID " + str(studentId) + " Notes"


@app.route('/students/<int:studentId>/notes/new', methods=['GET', 'POST'])
def _addStudentNotes(studentId):
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('newnote.html', student=student)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            note = request.form.get('note')
            notes = request.form.get('notes')
            newNote = Notes(student_id= studentId,
                              note= note,
                              date= valdate,
                              notes= notes)
            session.add(newNote)
            session.commit()
            flash('Student Note Saved')

        return redirect(url_for('_studentDetails',studentId= studentId))


@app.route('/students/<int:studentId>/notes/<int:notesId>/edit', methods=['GET', 'POST'])
def _editStudentNotes(studentId, notesId):
    student = getStudentById(studentId)
    note = getNote(notesId)
    if request.method == 'GET':
        return render_template('editnote.html', student=student, note=note)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            nnote = request.form.get('note')
            notes = request.form.get('notes')
            note.student_id = studentId
            note.grade = nnote
            note.date = valdate
            note.notes = notes
            session.add(note)
            session.commit()
            flash('Student Note Edited')

        return redirect(url_for('_studentDetails', studentId=studentId))


@app.route('/students/<int:studentId>/notes/<int:notesId>/delete', methods=['GET', 'POST'])
def _deleteStudentNotes(studentId, notesId):
    student = getStudentById(studentId)
    note = getNote(notesId)
    if request.method == 'GET':
        return render_template('deletenote.html', student=student)
    else:
        if request.form['submit'] == 'delete':
            deleteNote(notesId)
            flash('Student Note deleted')

        return redirect(url_for('_studentDetails', studentId=studentId))

@app.route('/students/<int:studentId>/payments')
def _showStudentPayments(studentId):
    return "Student ID " + str(studentId) + " Payments"


@app.route('/students/<int:studentId>/payments/new', methods=['GET', 'POST'])
def _addStudentPayments(studentId):
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('newpayment.html', student=student)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            payment = request.form.get('payment')
            notes = request.form.get('notes')
            newPayment = Payments(student_id=studentId,
                            payment=payment,
                            date=valdate,
                            notes=notes)
            session.add(newPayment)
            session.commit()
            flash('Student Payment Saved')

        return redirect(url_for('_studentDetails', studentId=studentId))

@app.route('/students/<int:studentId>/payments/<int:paymentsId>/edit', methods=['GET', 'POST'])
def _editStudentPayments(studentId, paymentsId):
    student = getStudentById(studentId)
    payment = getPayment(paymentsId)
    if request.method == 'GET':
        return render_template('editpayment.html', student=student, payment=payment)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            ppayment = request.form.get('payment')
            notes = request.form.get('notes')
            payment.student_id = studentId
            payment.payment = ppayment
            payment.date = valdate
            payment.notes = notes
            session.add(payment)
            session.commit()
            flash('Student Payment Edited')

        return redirect(url_for('_studentDetails', studentId=studentId))


@app.route('/students/<int:studentId>/payments/<int:paymentsId>/delete', methods=['GET', 'POST'])
def _deleteStudentPayments(studentId, paymentsId):
    student = getStudentById(studentId)
    payment = getPayment(paymentsId)
    if request.method == 'GET':
        return render_template('deletepayment.html', student=student)
    else:
        if request.form['submit'] == 'delete':
            deletePayment(paymentsId)
            flash('Student Payment deleted')

        return redirect(url_for('_studentDetails', studentId=studentId))


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