import json
from flask import Flask, request, jsonify
from services.profile import add_student, delete_student_by_id, get_student_by_id, update_student_details

# Initialize Flask app
app = Flask(__name__)


@app.route('/')
def index():
    return "<h1> This is the Ashesi Hub API for students profile</h1>"


@app.route('/register', methods=['POST'])
def register_student():
    
    student:json = json.loads(request.data)

    added_student = add_student(student)
    if added_student[0]:
        return jsonify({"message": "student registered successfully", "status": "success", "data": get_student_by_id(student['student_id'])[1]}), added_student[1]

    elif not added_student[0] and added_student[1] == 400:
        return jsonify({'message': "This student already exist", 'status': 'error'}), added_student[1]
    
    elif not added_student[0] and added_student[1] == 500:
        return jsonify({'message': "This was a problem registering", 'status': 'error'}), added_student[1]
    else:
        return jsonify({'message': "This student already exist", 'status': 'error'}), added_student[1]

   
@app.route('/remove_student/<int:id>', methods=['DELETE'])
def remove_student(id: int):
    delete_student = delete_student_by_id(id)
    if delete_student[0]:
        return jsonify({'message': 'student deleted successfully', 'status': 'success'}), 200

    elif delete_student[0] == False and delete_student[1] == 400:
        return jsonify({'message': "The 'student_id' key doesn't exist in the dictionary.", 'status': 'error'}), 400
    else:
        return jsonify({'message': 'student with that id does not exist', 'status': 'not found'}), 404


@app.route('/update_student/<int:id>', methods=['PUT'])
def update_student(id: int):
    student:json = json.loads(request.data)
    updated_student = update_student_details(id, student)

    if updated_student[0]:
        return jsonify({"message": "student updated successfully", "status": "success", "data": get_student_by_id(id)[1]}), updated_student[1]

    elif not updated_student[0] and updated_student[1] == 404 :
        return jsonify({"message": "No student with the given id exist", "status": "error"}), updated_student[1]
    
    elif not updated_student[0] and updated_student[1] == 500 :
        return jsonify({"message": "Error updating student", "status": "error"}), updated_student[1]


@app.route('/get_student/<int:id>', methods=['GET'])
def get_student(id: int):
    student = get_student_by_id(id)
    if student[0]:
        return jsonify({"message": "successfull", "status": "success", "data": student[1]}), student[2]

    return jsonify({"message": "No student with that id exist", "status": "Not found error"}), student[2]


if __name__ == "__main__":
    app.run(debug=True, port=8080)