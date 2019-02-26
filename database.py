# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
# from sqlalchemy.pool import StaticPool
# from passlib.apps import custom_app_context as pwd_context
# import random
# import string
# import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
#from routes import login, db



#Base = declarative_base()
# secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


# db.metadata.clear()

# class Students(db.Model):
#     __tablename__ = 'students'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     mobile = db.Column(db.String)
#     email = db.Column(db.String)
#     notes = db.Column(db.String)
#     father = db.Column(db.String)
#     mother = db.Column(db.String)

#     @property
#     def serialize(self):
#         return {
#                 'id': self.id,
#                 'name': self.name,
#                 'mobile': self.mobile,
#                 'email': self.email,
#                 'notes': self.notes,
#                 'father': self.father,
#                 'mother': self.mother
#         }


# class Parents(UserMixin, db.Model):
#     __tablename__ = 'parents'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     mobile = db.Column(db.String)
#     address = db.Column(db.String)
#     job = db.Column(db.String)
#     email = db.Column(db.String)
#     notes = db.Column(db.String)
#     sex = db.Column(db.String)
#     username = db.Column(db.String)
#     password_hash = db.Column(db.String)
#     admin = db.Column(db.Integer, default=0)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)


#     @property
#     def serialize(self):
#         return {
#                 'id': self.id,
#                 'name': self.name,
#                 'mobile': self.mobile,
#                 'address': self.address,
#                 'job': self.job,
#                 'email': self.email,
#                 'notes': self.notes,
#                 'sex': self.sex
#         }


#     @login.user_loader
#     def load_user(id):
#         return Parents.query.get(int(id))



# class Grades(db.Model):
#     __tablename__ = 'grades'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, ForeignKey('students.id'))
#     grade = db.Column(db.String)
#     date = db.Column(db.DateTime, default=datetime.datetime.now)
#     notes = db.Column(db.String)


# class Notes(db.Model):
#     __tablename__ = 'notes'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, ForeignKey('students.id'))
#     note = db.Column(db.String)
#     date = db.Column(db.DateTime, default=datetime.datetime.now)
#     notes = db.Column(db.String)


# class Payments(db.Model):
#     __tablename__ = 'payments'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, ForeignKey('students.id'))
#     payment = db.Column(db.String)
#     date = db.Column(db.DateTime, default=datetime.datetime.now)
#     notes = db.Column(db.String)


# engine = create_engine('sqlite:///db.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
# db.metadata.create_all(engine)