import random
import json


class CourseGraph:
    def __init__(self):
        self.prerequisites = {}

    def add_course(self, course):
        if course not in self.prerequisites:
            self.prerequisites[course] = []

    def add_prerequisite(self, course, prerequisite):
        if course == prerequisite:
            raise ValueError(f"Course {course} can not be prerequisite.")
        if course not in self.prerequisites:
            raise ValueError(f"Course {course} does not exist.")
        if prerequisite not in self.prerequisites:
            raise ValueError(f"Prerequisite {prerequisite} does not exist.")

        if self.check_cycle(course, prerequisite):
            raise Exception(
                f"Adding {prerequisite} as a prerequisite of {course} creates a cycle."
            )

        self.prerequisites[course].append(prerequisite)

    def check_cycle(self, start, end, visited=None):
        if visited is None:
            visited = set()

        visited.add(start)

        for neighbor in self.prerequisites[start]:
            if neighbor == end or (
                neighbor not in visited and self.check_cycle(neighbor, end, visited)
            ):
                return True
        visited.remove(start)
        return False

    def get_prerequisites(self, course):
        return self.prerequisites.get(course, [])

    def is_valid_prerequisite(self, course, prerequisite):
        try:
            self.add_prerequisite(course, prerequisite)
            return True
        except Exception:
            return False

    def add_prerequisite_if_valid(self, course, prerequisite):
        if course != prerequisite and not self.check_cycle(course, prerequisite):
            self.prerequisites[course].append(prerequisite)
            return True
        return False


if __name__ == "__main__":
    # num of tracks
    n_track = 5
    tracks = ["Track_" + str(i) for i in range(n_track)]
    # num of courses
    n_course = 20
    courses = ["COMS" + str(i) for i in range(n_course)]
    # required courses for each track
    n_required = n_course // 5

    # dependancy graphs
    # required course for each track
    track_required = {}
    for i, t in enumerate(tracks):
        r_qs = [courses[(i + j) % len(courses)] for j in range(n_required)]
        track_required[t] = r_qs

    # generate required pre for each course
    prerequisites = CourseGraph()
    for c in courses:
        prerequisites.add_course(c)

    for c in courses:
        potential_prerequisites = set(courses[: courses.index(c)])
        for _ in range(n_course // 4):
            if potential_prerequisites:
                pre_course = random.choice(list(potential_prerequisites))
                prerequisites.add_prerequisite_if_valid(c, pre_course)
                potential_prerequisites.remove(pre_course)

    result = {"courses": prerequisites.prerequisites, "track": track_required}

    with open("dummy_data.json", "w") as json_file:
        json.dump(result, json_file, indent=4)
