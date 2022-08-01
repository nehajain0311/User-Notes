from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#two database table one is NOTE to keep all the notes
#other to store all the users
# this is our database table schema

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #this will automatically will get the date from func and set it
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user is in lower case when setting foreing key for SQLALchmey


class User(db.Model, UserMixin): #multiple inheritance, we used USerMixin just for User LOgin
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #sets the relationship between each user and its notes, Note is in capital when setting relationship
