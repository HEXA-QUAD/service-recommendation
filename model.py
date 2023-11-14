from datetime import datetime
import time
from sqlalchemy.dialects.postgresql import JSONB
import json
from common import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String


class Track(db.Model):
    tid = db.Column(db.String(256), primary_key=True)
    track_name = db.Column(db.String(80), unique=True, nullable=False)
    required_courses = db.Column(db.JSON)  # list of required course {id:name}

    def __repr__(self):
        return f"<Track {self.name}>"

    def to_dict(self):
        return {
            "tid": self.tid,
            "track_name": self.track_name,
            "required_courses": self.required_courses,
        }

class Course(db.Model):
    cid = db.Column(db.String(256), primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    prerequisites = db.Column(db.JSON)  # list of prerequiste courses {id:name}

    def __repr__(self):
        return f"<Course {self.name}>"

    def to_dict(self):
        return {
            "cid": self.cid,
            "course_name": self.course_name,
            "prerequisites": self.prerequisites,
        }


class StudentHistory(db.Model):
    hid = db.Column(db.String(256), primary_key=True)
    uni = db.Column(db.String(80))
    semester = db.Column(db.String(80))
    year = db.Column(db.Integer)
    track_name = db.Column(db.String(80))
    courses = db.Column(db.JSON)  # list of course taken during this semester
    time_stamp = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Student history {self.uni}>"

    def to_dict(self):
        return {
            "hid": self.hid,
            "uni": self.uni,
            "semester": self.semester,
            "year": self.year,
            "track_name": self.track_name,
            "courses": self.courses,
            "time_stamp": self.time_stamp,
        }


class Recommendation(db.Model):
    rid = db.Column(db.String(256), primary_key=True)
    time_stamp = db.Column(db.DateTime, server_default=db.func.now())
    hid = db.Column(db.String(256))
    content = db.Column(db.JSON)  # reocommandation content

    def __repr__(self):
        return f"<Recommendation {self.time_stamp}>"

    def to_dict(self):
        return {
            "rid": self.rid,
            "time_stamp": self.time_stamp,
            "hid": self.hid,
            "content": self.content,
        }


# class prerequisite(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     course_cid = db.Column(db.Integer)
#     prerequisite_cid = db.Column(db.Integer)