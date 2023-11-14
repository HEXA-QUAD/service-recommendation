from flask import request, jsonify
from common import app, db
from config import Config
import util
import model
from model import StudentHistory, Recommendation, Course, Track


"""
Course section
"""


@app.route("/api/get_course", methods=["GET"])
def get_course():
    course_name = request.json.get("course_name")
    course = db.session.execute(
        db.select(Course).filter_by(course_name=course_name)
    ).scalar_one()
    result = course.to_dict()
    return jsonify({"msg": "success", "data": result})


@app.route("/api/add_course", methods=["POST"])
def add_course():
    # add or update
    course_name = request.json.get("course_name")
    prerequisites = request.json.get("prerequisites")
    courses = db.session.query(Course).filter_by(course_name=course_name)
    if courses.count() == 0:
        course = Course(
            cid=util.generate_id("C"),
            course_name=course_name,
            prerequisites=prerequisites,
        )
        db.session.add(course)
        message = "Course updated"

    else:
        course = courses.first()
        course.course_name = course_name
        course.prerequisites = prerequisites
        message = "Course Added"

    db.session.commit()
    print(course.to_dict())
    return jsonify({"msg": message})


"""
Track section
"""


@app.route("/api/get_track", methods=["GET"])
def get_track():
    data = request.get_json()
    track_name = data["track_name"]
    try:
        tracks = Track.query.filter_by(track_name=track_name)
        if tracks.count() > 0:
            track = tracks.first()
            result = track.to_dict()
            return jsonify({"msg": "success", "data": result})
        else:
            return jsonify({"msg": "no entry"})
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/api/add_track", methods=["POST"])
def add_track():
    data = request.get_json()
    if not data or "track_name" not in data or "required_courses" not in data:
        return {"message": "Missing data"}, 400

    tid = util.generate_id("T")
    track_name = data["track_name"]
    required_courses = data["required_courses"]

    try:
        tracks = Track.query.filter_by(track_name=track_name)
        if tracks.count() > 0:
            track = tracks.first()
            track.track_name = track_name
            track.required_courses = required_courses
            message = "Track updated"
        else:
            track = Track(
                tid=tid, track_name=track_name, required_courses=required_courses
            )
            db.session.add(track)
            message = "New track added"
        print(track.to_dict())
        db.session.commit()

        return {"msg": message}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


"""
Student History section
"""


@app.route("/api/add_student_history", methods=["POST"])
def add_student_history():
    uni = request.json.get("uni")
    courses = request.json.get("courses")  # enfore sanity checking
    semester = request.json.get("semester")
    track_name = request.json.get("track_name")
    year = request.json.get("year")

    hid = util.generate_id("S")
    history = model.StudentHistory(
        hid=hid,
        uni=uni,
        courses=courses,
        semester=semester,
        year=year,
        track_name=track_name,
    )
    db.session.add(history)
    db.session.commit()
    return jsonify({"msg": "Student history added"})


@app.route("/api/get_student_history", methods=["POST"])
def get_student_history():
    uni = request.json.get("uni")
    semester = request.json.get("semester")
    history = StudentHistory.query.filter_by(uni=uni, semester=semester).get_or_404()
    print(history)
    return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    # with app.app_context():
    #     db.create_all()
