from datetime import datetime
import time
from sqlalchemy.dialects.postgresql import JSONB
import json
from common import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column



class Track(db.Model):
    tid = db.Column(db.String(256), primary_key=True)
    track_name = db.Column(db.String(80), unique=True, nullable=False)
    required_course = db.Column(db.JSON) #list of required course {id:name}
    def __repr__(self):
        return f'<Track {self.name}>'

class Course(db.Model):
    cid = db.Column(db.String(256), primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    prerequisites = db.Column(db.JSON)  # list of prerequiste courses {id:name}
    def __repr__(self):
        return f'<Course {self.name}>'
 
class StudentHistory(db.Model):
    sid = db.Column(db.String(256), primary_key=True)
    uni = db.Column(db.String(80))
    semester = db.Column(db.String(80))
    year = db.Column(db.Integer)
    track_name = db.Column(db.String(80))
    courses = db.Column(db.JSON) # list of course taken during this semester
    def __repr__(self):
        return f'<Student history {self.uni}>'

# class prerequisite(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     course_cid = db.Column(db.Integer)
#     prerequisite_cid = db.Column(db.Integer)



