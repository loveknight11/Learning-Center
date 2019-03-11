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



@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

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
    grades = student.all_grades
    notes = student.all_notes
    payments = student.all_payments
    parent = getParentById(current_user.parent_id)
    if parent in student.parents or current_user.admin == 1:
        return render_template('student.html', student=student, notes=notes, grades=grades, payments=payments)
    else:
        return "Not allowed to view this page"

# New Student
@app.route('/students/new', methods=['GET', 'POST'])
@login_required
def _newStudent():
    if not is_admin():
        return "Not allowed to view this page"
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
            if (not checkParent(father) and father):
                flash("father is not in our database, please add his info")
                return render_template('newstudent.html', name=name,
                    mobile=mobile,
                    email=email,
                    notes=notes,
                    mother=mother)

            if (not checkParent(mother) and mother):
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
    if not is_admin():
        return "Not allowed to view this page"
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
            if (not checkParent(father) and father):
                flash("father is not in our database, please add his info")
                return render_template('editstudent.html', student=student)

            if (not checkParent(mother) and mother):
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
    if not is_admin():
        return "Not allowed to view this page"
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('deletestudent.html', student=student)
    else:
        if request.form['submit'] == 'delete':
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
    if not is_admin():
        return "Not allowed to view this page"
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('newgrade.html', student=student)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            grade = request.form.get('grade')
            notes = request.form.get('notes')
            addGrade(studentId, grade, valdate, notes)
            flash('Student Grade Saved')

        return redirect(url_for('_studentDetails',studentId= studentId))

# Edit Grade
@app.route('/students/<int:studentId>/grades/<int:gradesId>/edit', methods=['GET', 'POST'])
@login_required
def _editStudentGrades(studentId, gradesId):
    if not is_admin():
        return "Not allowed to view this page"
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
            editGrade(grade, studentId, ggrade, valdate, notes)
            flash('Student Grade Edited')

        return redirect(url_for('_studentDetails', studentId=studentId))

# Delete Grade
@app.route('/students/<int:studentId>/grades/<int:gradesId>/delete', methods=['GET', 'POST'])
@login_required
def _deleteStudentGrades(studentId, gradesId):
    if not is_admin():
        return "Not allowed to view this page"
    student = getStudentById(studentId)
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
    if not is_admin():
        return "Not allowed to view this page"
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('newnote.html', student=student)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            note = request.form.get('note')
            notes = request.form.get('notes')
            addNote(studentId, note, valdate, notes)
            flash('Student Note Saved')

        return redirect(url_for('_studentDetails',studentId= studentId))

# Edit Notes
@app.route('/students/<int:studentId>/notes/<int:notesId>/edit', methods=['GET', 'POST'])
@login_required
def _editStudentNotes(studentId, notesId):
    if not is_admin():
        return "Not allowed to view this page"
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
            editNote(note, studentId, nnote, valdate, notes)
            flash('Student Note Edited')

        return redirect(url_for('_studentDetails', studentId=studentId))

# Delete Notes
@app.route('/students/<int:studentId>/notes/<int:notesId>/delete', methods=['GET', 'POST'])
@login_required
def _deleteStudentNotes(studentId, notesId):
    if not is_admin():
        return "Not allowed to view this page"
    student = getStudentById(studentId)
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
    if not is_admin():
        return "Not allowed to view this page"
    student = getStudentById(studentId)
    if request.method == 'GET':
        return render_template('newpayment.html', student=student)
    else:
        if request.form['submit'] == 'save':
            date = request.form.get('date')
            valdate = datetime.strptime(date, "%Y-%m-%d").date()
            payment = request.form.get('payment')
            notes = request.form.get('notes')
            addPayment(studentId, payment, valdate, notes)
            flash('Student Payment Saved')

        return redirect(url_for('_studentDetails', studentId=studentId))

# Edit Payment
@app.route('/students/<int:studentId>/payments/<int:paymentsId>/edit', methods=['GET', 'POST'])
@login_required
def _editStudentPayments(studentId, paymentsId):
    if not is_admin():
        return "Not allowed to view this page"
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
            editPayment(payment, studentId, ppayment, valdate, notes)
            flash('Student Payment Edited')

        return redirect(url_for('_studentDetails', studentId=studentId))

# Delete Payment
@app.route('/students/<int:studentId>/payments/<int:paymentsId>/delete', methods=['GET', 'POST'])
@login_required
def _deleteStudentPayments(studentId, paymentsId):
    if not is_admin():
        return "Not allowed to view this page"
    student = getStudentById(studentId)
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
    if not is_admin():
        return "Not allowed to view this page"
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
    if not is_admin() and current_user.parent_id != parentId:
        return "Not allowed to view this page"
    parent = getParentById(parentId)
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
    if not is_admin():
        return "Not allowed to view this page"
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


@app.route('/courses/new', methods=['GET', 'POST'])
@login_required
def _addCourse():
    if request.method == 'POST':
        if request.form['submit'] == 'save':
            name = request.form.get('course')
            notes = request.form.get('notes')
            addCourse(name=name, notes=notes)

        return redirect(url_for('_allCourses'))

    if is_admin():
        return render_template('newcourse.html')
    else:
        return 'Not Allowed'

@app.route('/courses')
@login_required
def _allCourses():
    courses = getAllCourses()
    return render_template('allcourses.html', courses=courses)


@app.route('/courses/<int:courseId>/edit', methods=['GET', 'POST'])
@login_required
def _editCourse(courseId):
    if not is_admin():
        return "Not Allowed"
    course = getCourseById(courseId)
    if request.method == 'POST':
        if request.form['submit'] == 'save':
            course.name = request.form.get('course')
            course.notes = request.form.get('notes')
            editCourse(course)

        return redirect(url_for('_allCourses'))

    return render_template('editcourse.html', course=course)


@app.route('/locations/new', methods=['GET', 'POST'])
@login_required
def _addLocation():
    if not is_admin():
        return "Not allowed"
    if request.method == 'POST':
        if request.form['submit'] == 'save':
            loc = request.form.get('location')
            notes = request.form.get('notes')
            addLocation(name=loc, notes=notes)

        return redirect(url_for('_allLocations'))

    return render_template('newlocation.html')


@app.route('/locations/<int:locationId>/edit', methods=['GET', 'POST'])
@login_required
def _editLocation(locationId):
    if not is_admin():
        return "Not Allowed"
    location = getLocationById(locationId)
    if request.method == 'POST':
        if request.form['submit'] == 'save':
            location.name = request.form.get('location')
            location.notes = request.form.get('notes')
            editLocation(location)

        return redirect(url_for('_allLocations'))

    return render_template('editlocation.html', location=location)


@app.route('/locations')
@login_required
def _allLocations():
    locations = getAllLocations()
    return render_template('allLocations.html', locations=locations)


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
        username = request.form.get('username').lower()
        password = request.form.get('password')
        user = getUserByUsername(username)
        if user is None or not user.check_password(password=password):
            flash('Wrong Username or password')
            return render_template('login.html')
        else:
            flash('Welcome ' + user.username)
            login_user(user, True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('_showIndex')
            return redirect(next_page)

@app.route('/logout')
@login_required
def _logout():
    logout_user()
    return render_template('index.html')


@app.route('/username/change', methods=['GET', 'POST'])
@login_required
def _changeUsername():
    if request.method == 'POST':
        if request.form['submit'] == 'save':
            newUsername = request.form.get('new').lower()
            if not newUsername or newUsername == current_user.username:
                flash('Username not Change')
                return redirect(url_for('_showIndex'))
            else:
                if checkUsernameAvailable(newUsername):
                    editUsername(current_user.parent_id, newUsername)
                    _logout()
                    flash('Username Changed, Login with new username')
                    return redirect(url_for('_login'))
                else:
                    flash('Username is not valid')
                    return redirect(url_for('_changeUsername'))
        else:
            return redirect(url_for('_showIndex'))
    return render_template('changeusername.html', username=current_user.username)


@app.route('/password/change', methods=['GET', 'POST'])
@login_required
def _changePassword():
    if request.method == 'POST':
        if request.form['submit'] == 'save':
            current = request.form.get('current')
            new = request.form.get('new')
            re = request.form.get('re')
            if new == re:
                if current_user.check_password(current):
                    editPassword(current_user.parent_id, new)
                    _logout()
                    flash('Password Changed, Login with new password')
                    return redirect(url_for('_login'))
                else:
                    flash('Wrong Current Password')
                    return redirect(url_for('_changePassword'))
            else:
                flash('passwords donot match')
                return redirect(url_for('_changePassword'))
        else:
            return redirect(url_for('_showIndex'))


    return render_template('changepassword.html')


@app.route('/parents/json')
@login_required
def getParentsJson():
    parents = getAllParents()
    return jsonify([parent.serialize for parent in parents])



@app.route('/fathers/json')
@login_required
def getFathersJson():
    if not is_admin():
        return "Not allowed to view this page"
    fathers = getAllFathers()
    return jsonify([father.serialize for father in fathers])


@app.route('/mothers/json')
@login_required
def getMothersJson():
    if not is_admin():
        return "Not allowed to view this page"
    mothers = getAllMothers()
    return jsonify([mother.serialize for mother in mothers])


@app.route('/students/json')
@login_required
def getStudentsJson():
    if not is_admin():
        return "Not allowed to view this page"
    students = getAllStudents()
    return jsonify([student.serialize for student in students])


@app.route('/courses/json')
@login_required
def getCoursesJson():
    courses = getAllCourses()
    return jsonify([course.serialize for course in courses])


@app.route('/locations/json')
@login_required
def getLocationsJson():
    locations = getAllLocations()
    return jsonify([location.serialize for location in locations])


def is_admin():
    if current_user.admin == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000')
    insertAdminUser()
    #app.run()