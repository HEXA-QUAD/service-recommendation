import requests
import json


api_add_course = "http://3.144.39.6:5000/api/add_course"  
api_add_track = "http://3.144.39.6:5000/api/add_track"  

with open("gpt_dummy_1.json", "r") as json_file:
    # Parse the JSON data into a Python dictionary
    data = json.load(json_file)


# Prepare the JSON data as a Python dictionary
courses = data["courses"]
track = data["track"]

courses_prep_data = []
track_prep_data = []

for cname, pres in courses.items():
    temp = {"course_name": cname, "prerequisites": pres}
    courses_prep_data.append(temp)

for tname, reqs in track.items():
    temp = {"track_name": tname, "required_courses": reqs}
    track_prep_data.append(temp)

for d in courses_prep_data:
    response = requests.post(api_add_course, json=d)
for d in track_prep_data:
    response = requests.post(api_add_track, json=d)
