import json
from typing import Any, Dict, List, Tuple, Union
from config.db import db

students_ref = db.collection(u'students')

def get_all_students() -> List[Dict[str, Any]]:
    students = students_ref.stream()
    return [student.to_dict() for student in students]


def get_student_by_id(id: int) -> Tuple[bool, Dict[str, Any], int]:
    student = students_ref.document(str(id)).get()
    if student.exists:
        return True, student.to_dict(), 200
    else:
        return False, {}, 404


def add_student(student:json)-> Tuple[bool, int]:
    try:
        student_exists = students_ref.where("student_id", "==", student['student_id']).get()
        if student_exists:
            return False, 409
        students_ref.document(str(student.get('student_id'))).set(student)
        return True, 200
    except Exception:
        return False, 500


def delete_student_by_id(id: int) -> Tuple[bool, int]:
    student = get_student_by_id(id)
    if(student[0]):
        try:
            students_ref.document(str(id)).delete()
            return True, 200
        except Exception:
            return False, 500
    return False, 404


def update_student_details(id: int, updated_student: Dict[str, Any]) -> Tuple[bool, int]:
    student = get_student_by_id(id)
    if student[0]:
        try:
            student_ref = db.collection(u'students').document(str(id))
            student_ref.set(updated_student, merge=True)
            # students_ref.document(str(id)).update(updated_student)
            return True, 200
        except Exception:
            return False, 500
    return False, 404