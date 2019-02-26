import sys
from flask import *
from config import Config
from datetime import datetime
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.urls import url_parse


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = '_login'


from database_functions import *
from models import *

# Main Page
@app.route('/')
def _showIndex():
    return render_template('index.html')

# All Students
@app.route('/students', methods=['GET', 'POST'])
@login_required
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

# Student Details
@app.route('/students/<int:studentId>')
@login_required
def _studentDetails(studentId):
    student = getStudentById(studentId)
    grades = getStudentGrades(studentId)
    notes = getStudentNotes(studentId)
    payments = getStudentPayments(studentId)
    return render_template('student.html', student=student, notes=notes, grades=grades, payments=payments)

# New Student
@app.route('/students/new', methods=['GET', 'POST'])
@login_required
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


# Edit Student
@app.route('/students/<int:studentId>/edit', methods=['GET', 'POST'])
@login_required
def _editStudent(studentId):
    student = getStudentById(studentId)
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

# Delete Student
@app.route('/students/<int:studentId>/delete', methods=['GET', 'POST'])
@login_required
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

# Add Grade
@app.route('/students/<int:studentId>/grades/new', methods=['GET', 'POST'])
@login_required
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

# Edit Grade
@app.route('/students/<int:studentId>/grades/<int:gradesId>/edit', methods=['GET', 'POST'])
@login_required
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

# Delete Grade
@app.route('/students/<int:studentId>/grades/<int:gradesId>/delete', methods=['GET', 'POST'])
@login_required
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

# Add Notes
@app.route('/students/<int:studentId>/notes/new', methods=['GET', 'POST'])
@login_required
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

# Edit Notes
@app.route('/students/<int:studentId>/notes/<int:notesId>/edit', methods=['GET', 'POST'])
@login_required
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

# Delete Notes
@app.route('/students/<int:studentId>/notes/<int:notesId>/delete', methods=['GET', 'POST'])
@login_required
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

# Add Payment
@app.route('/students/<int:studentId>/payments/new', methods=['GET', 'POST'])
@login_required
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

# Edit Payment
@app.route('/students/<int:studentId>/payments/<int:paymentsId>/edit', methods=['GET', 'POST'])
@login_required
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

# Delete Payment
@app.route('/students/<int:studentId>/payments/<int:paymentsId>/delete', methods=['GET', 'POST'])
@login_required
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

# Add Parent
@app.route('/parents/new', methods=['GET', 'POST'])
@login_required
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
            username = request.form.get('username')
            password = request.form.get('password')
            if checkUsernameAvailable(username):
                addNewParent(name=name, sex=sex, mobile=mobile, address=address, job=job, email=email, notes=notes, username=username, password=password)
                flash('Parent Added Successfully')
                return redirect(url_for('_showIndex'))
            else:
                flash('User Name Already Exists')
                render_template('newparent.html',
                                name=name,
                                sex=sex,
                                mobile=mobile,
                                address=address,
                                job=job,
                                email=email,
                                notes=notes)
        else :
            return redirect(url_for('_showIndex'))

# Edit Parent
@app.route('/parents/<int:parentId>/edit', methods=['GET', 'POST'])
@login_required
def _editParent(parentId):
    parent = getParentById(parentId)
    students = getStudentsForParent(parent.name)
    if request.method == 'GET':
        return render_template('editparent.html', parent=parent)
    else:
        if request.form['submit'] == 'save':
            name = request.form.get('name')
            mobile = request.form.get('mobile')
            address = request.form.get('address')
            job = request.form.get('job')
            email = request.form.get('email')
            notes = request.form.get('notes')
            sex = request.form.get('sex')
            username = request.form.get('username')

            if not checkEditUsernameAvailable(parent.id, username):
                flash('User Name Already Exists')
                return render_template('editparent.html', parent=parent)

            if parent.name != name:
                editStudentParentName(parent.name, name)

            editParent(parent.id, name, mobile, address, job, email, notes, sex)

            flash('Parent Information Updated')
            parents = getAllParents()
            return render_template('allparents.html', parents=parents)
        else:
            return redirect(url_for('_showAllParents'))


# Delete Parent
@app.route('/parents/<int:parentId>/delete', methods=['GET', 'POST'])
@login_required
def _deleteParent(parentId):
    parent = getParentById(parentId)
    students = getStudentsForParent(parent.name)
    if request.method == 'GET':
        if students:
            flash('Parent can not be deleted as he has registered Students under his name')
            return redirect(url_for('_showAllParents'))
        else:
            return render_template('deleteparent.html', parent=parent)
    else:
        if request.form['submit'] == 'delete':
            deleteParent(parentId)
            flash('Parent deleted')
        return redirect(url_for('_showAllParents'))




@app.route('/parents', methods=['GET', 'POST'])
@login_required
def _showAllParents():
    if request.method == 'POST':
        name = request.form.get('search')
        parent = getParentByName(name)
        if parent:
            return render_template('allparents.html', parents=parent)
        else:
            flash('Parent name is not in our database')
            parents = getAllParents()
            render_template('allparents.html', parents=parents)
    parents = getAllParents()
    return render_template('allparents.html', parents = parents)

@app.route('/cv')
def _getCV():
    return render_template('cv.html')


@app.route('/login', methods=['GET', 'POST'])
def _login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('index.html')
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        parent = getParentByUsername(username)
        if parent is None or not parent.check_password(password=password):
            flash('Wrong Username or password')
            return render_template('login.html')
        else:
            flash('Welcome ' + parent.name)
            login_user(parent)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('_showIndex')
            return redirect(next_page)

@app.route('/logout')
@login_required
def _logout():
    logout_user()
    return render_template('index.html')


@app.route('/parents/json')
@login_required
def getParentsJson():
    parents = getAllParents()
    return jsonify([parent.serialize for parent in parents])



@app.route('/fathers/json')
@login_required
def getFathersJson():
    fathers = getAllFathers()
    return jsonify([father.serialize for father in fathers])


@app.route('/mothers/json')
@login_required
def getMothersJson():
    mothers = getAllMothers()
    return jsonify([mother.serialize for mother in mothers])


@app.route('/students/json')
@login_required
def getStudentsJson():
    students = getAllStudents()
    return jsonify([student.serialize for student in students])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000')