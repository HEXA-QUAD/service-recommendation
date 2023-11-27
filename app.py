from flask import request, jsonify
from common import app, db
from config import Config
import util
import model
from model import Recommendation, Course, Track
import recommendation.recommendation as R

"""
Course section
"""


@app.route("/api/get_course", methods=["GET"])
def get_course():
    course_name = request.args.get("course_name", None)
    # course_name = request.json.get("course_name")
    if course_name:
        course = db.session.execute(
            db.select(Course).filter_by(course_name=course_name)
        ).scalar_one()
        result = course.to_dict()
    else:
        courses = Course.query.all()
        result = [c.to_dict() for c in courses]
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


@app.route("/api/remove_course", methods=["DELETE"])
def remove_course():
    cid = request.json.get("cid")
    course = db.session.query(Course).filter_by(cid=cid).first()
    if not course:
        return jsonify({"msg": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({"msg": "Course successfully removed"}), 200


@app.route("/api/update_course", methods=["PUT"])
def update_course():
    cid = request.json.get("cid")
    course_name = request.json.get("course_name")
    prerequisites = request.json.get("prerequisites")
    course = db.session.query(Course).filter_by(cid=cid).first()
    if not course:
        return jsonify({"msg": "Course not found"}), 404
    course.course_name = course_name
    course.prerequisites = prerequisites
    db.session.commit()

    return jsonify({"msg": "Course successfully updated"}), 200


"""
Track section
"""


@app.route("/api/get_track", methods=["GET"])
def get_track():
    # data = request.get_json()
    track_name = request.args.get("track_name", None)
    # track_name = data["track_name"]
    try:
        if track_name:
            tracks = Track.query.filter_by(track_name=track_name)
            if tracks.count() > 0:
                track = tracks.first()
                result = track.to_dict()
                return jsonify({"msg": "success", "data": result})
            else:
                return jsonify({"msg": "no entry"})
        else:
            tracks = Track.query.all()
            return jsonify({"msg": "success", "data": [t.to_dict() for t in tracks]})

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


@app.route("/api/remove_track", methods=["DELETE"])
def remove_track():
    tid = request.json.get("tid")
    track = db.session.query(Track).filter_by(tid=tid).first()
    if not track:
        return jsonify({"msg": "Track not found"}), 404

    db.session.delete(track)
    db.session.commit()

    return jsonify({"msg": "Track successfully removed"}), 200


@app.route("/api/update_track", methods=["PUT"])
def update_track():
    tid = request.json.get("tid")
    track_name = request.json.get("track_name")
    required_courses = request.json.get("required_courses")

    track = db.session.query(Track).filter_by(tid=tid).first()
    if not track:
        return jsonify({"msg": "Track not found"}), 404

    track.track_name = track_name
    track.required_courses = required_courses

    db.session.commit()

    return jsonify({"msg": "Track successfully updated"}), 200


"""
Student History section
"""


# @app.route("/api/add_student_history", methods=["POST"])
# def add_student_history():
#     uni = request.json.get("uni")
#     courses = request.json.get("courses")  # enfore sanity checking
#     semester = request.json.get("semester")
#     track_name = request.json.get("track_name")
#     year = request.json.get("year")

#     hid = util.generate_id("S")
#     history = model.StudentHistory(
#         hid=hid,
#         uni=uni,
#         courses=courses,
#         semester=semester,
#         year=year,
#         track_name=track_name,
#     )
#     db.session.add(history)
#     db.session.commit()
#     return jsonify({"msg": "Student history added"})


# @app.route("/api/get_student_history", methods=["GET"])
# def get_student_history():
#     all = request.args.get("all")
#     uni = request.json.get("uni")
#     semester = request.json.get("semester")
#     history = StudentHistory.query.filter_by(uni=uni, semester=semester)
#     if history.count() == 0:
#         return jsonify({"msg": "no history"})
#     if all:
#         result = []
#         for h in history:
#             result.append(h.to_dict())
#         msg = "get all"
#     else:
#         history = history.order_by(StudentHistory.created_at).first()
#         result = history.to_dict()
#         msg = "get most recent"
#     return jsonify({"msg": msg, "data": result})


"""
Recommendation section

1. base on the student tracks
2. base on the taken courses

Note:
1. need to have the student previous history
"""


@app.route("/api/get_recommendation", methods=["GET"])
def get_recommendation():
    # get the most recent recommendation
    all = request.args.get("all")
    uni = request.args.get("uni")
    # data = request.get_json()
    # uni = data["uni"]
    recommendation = Recommendation.query.filter_by(uni=uni).order_by(
        Recommendation.created_at.desc()
    )
    if recommendation.count() == 0:
        return jsonify({"msg": "no recommendation yet"})

    if all:
        result = []
        for h in recommendation:
            result.append(h.to_dict())
        msg = "get all"
        return jsonify({"msg": msg, "data": result})
    else:
        recommendation = recommendation.first()
        result = recommendation.to_dict()
        msg = "get most recent"
        return jsonify({"msg": msg, "data": result})


@app.route("/api/create_recommendation", methods=["POST"])
def create_recommendation():
    """create recommendation base on the most recent history"""
    data = request.get_json()
    uni = data["uni"]
    courses_taken = data["courses_taken"]  # list of the taken courses
    track_name = data["track_name"]

    # history = (
    #     StudentHistory.query.filter_by(uni=uni)
    #     .order_by(StudentHistory.created_at.desc())
    #     .first()
    # )
    # if not history:
    #     return jsonify({"msg": "no student history yet"}), 404
    # courses_taken = history.courses
    # track_name = history.track_name

    track = Track.query.filter_by(track_name=track_name).first()
    if not track:
        return jsonify({"msg": "Track not found"}), 404

    track_courses = track.required_courses

    ok, missing_courses = R.can_graduate(courses_taken, track_courses)
    if ok:
        return jsonify({"msg": "Already fullfilled the requirements"})

    all_course = Course.query.all()
    all_course_mp = {}
    for c in all_course:
        t = c.to_dict(keys=["course_name", "prerequisites"])
        all_course_mp[t["course_name"]] = t["prerequisites"]
    ok, seq = R.suggest_course_sequence(courses_taken, missing_courses, all_course_mp)
    if ok:
        r = model.Recommendation(
            rid=util.generate_id("R"),
            uni=uni,
            content={"plan_seq": seq},
        )
        db.session.add(r)
        db.session.commit()
        return jsonify({"msg": "success", "data": seq})
    return jsonify({"msg": "encounter error"})


@app.route("/api/fufilled_course_prerequisites", methods=["POST"])
def fufilled_course_prerequisites():
    data = request.get_json()
    courses_taken = data["courses_taken"]  # list of the taken courses
    target_course = data["target_course"]
    course = db.session.query(Course).filter_by(course_name=target_course).first()
    if not course:
        return jsonify({"msg": "Course not found"}), 404
    status, _ = R.can_graduate(courses_taken, course.prerequisites)
    if status:
        #fufilled
        return jsonify({"msg": "Fufilled"}), 200
    else:
        return jsonify({"msg": "Not Fufilled"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

    # with app.app_context():
    #     db.create_all()
