from routes import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    parent_id = db.Column(db.Integer)
    admin = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


parentStudent = db.Table('parentStudent',
    db.Column('parent_id', db.Integer, db.ForeignKey('parents.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True)
    )

class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mobile = db.Column(db.String)
    address = db.Column(db.String)
    job = db.Column(db.String)
    email = db.Column(db.String)
    notes = db.Column(db.String)
    sex = db.Column(db.String)
    students = db.relationship('Students', secondary=parentStudent, lazy='subquery', backref=db.backref('parents', lazy=True))


    @property
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'mobile': self.mobile,
                'address': self.address,
                'job': self.job,
                'email': self.email,
                'notes': self.notes,
                'sex': self.sex
        }


class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mobile = db.Column(db.String)
    email = db.Column(db.String)
    notes = db.Column(db.String)
    father = db.Column(db.String)
    mother = db.Column(db.String)

    @property
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'mobile': self.mobile,
                'email': self.email,
                'notes': self.notes,
                'father': self.father,
                'mother': self.mother
        }


