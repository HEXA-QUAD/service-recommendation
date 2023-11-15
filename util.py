import uuid
from common import app, db



def generate_id(prefix):
    r = str(uuid.uuid4())
    r = prefix + "_" + r
    return r


def check_and_clean_courses(course_json):
    # check if the courses are valid
    # course {cid: name}
    pass

def check_and_clean_prerequisites(prerequisites_json):
    # check if the courses are valid
    # course {cid: name}
    pass


def check_and_clean_semester(semester_str):
    # check if the courses are valid
    semester_str = semester_str.lower()
    if semester_str != "fall" or semester_str != "spring" or semester_str != "summer":
        return False, ""
    return True, semester_str


def check_valid_year(year_int):
    # check if the courses are valid
    pass
