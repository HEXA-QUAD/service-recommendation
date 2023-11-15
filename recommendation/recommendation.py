"""recommendation utils"""


def can_graduate(taken_courses, required_courses):
    taken_courses = set(taken_courses) if taken_courses else set()
    required_courses = set(required_courses) if required_courses else set()
    missing_courses = list(required_courses - taken_courses)
    if required_courses.issubset(taken_courses):
        return True, set()
    else:
        return False, missing_courses


def plan_courses(taken_courses, missing_courses, all_courses_mp):
    print(missing_courses, "missing mp \n")
    print(taken_courses, "taken\n")
    print(all_courses_mp, "all\n")

    return


def suggest_course_sequence(taken_courses, missing_courses, all_courses_map):
    print(taken_courses, missing_courses, all_courses_map)
    if taken_courses is None:
        taken_courses = []
    if missing_courses is None:
        missing_courses = []
    courses_planned = set(taken_courses)
    suggested_sequence = []

    def add_course_with_prerequisites(course):
        if course in courses_planned:
            return True
        for prereq in all_courses_map.get(course, []):
            if prereq not in courses_planned and not add_course_with_prerequisites(
                prereq
            ):
                return False
        suggested_sequence.append(course)
        courses_planned.add(course)
        return True

    for course in missing_courses:
        if not add_course_with_prerequisites(course):
            print(
                f"Cannot complete the course {course} due to unfulfilled prerequisites."
            )
            return False, []

    return True, suggested_sequence
