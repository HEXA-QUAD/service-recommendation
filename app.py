from flask import request, jsonify
from common import app, db
from config import Config
import util
import model


@app.route("/api/update_student")
def update_student_history():
    uni = request.json.get("uni")
    courses = request.json.get("courses")
    semester = request.json.get("semester")
    track_name = request.json.get("track_name")
    sid = util.generate_id("S")
    record = db.one_or_404(db.select(model.StudentHistory).filter_by(uni=uni, semester=semester),
                           description=f"No uni named '{uni}'.")
    print(record)
    return jsonify({"ok": "123"})


@app.route("/api/")
def enroll_student():
    request.json.get("sid")
    request.json.get("cid")
    request.json.get("semester")
    return


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    with app.app_context():
        db.create_all()
