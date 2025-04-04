from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import cv2
import numpy as np
import base64
from datetime import datetime
import json
from face_detection import FaceDetectionSystem
from database import EmployeeDatabase

app = Flask(__name__)
app.secret_key = 'face_attendance_system_secret_key'

# Initialize the face detection system and database
face_system = FaceDetectionSystem()
db = EmployeeDatabase()

# Ensure directories exist
os.makedirs('data/employees', exist_ok=True)
os.makedirs('data/temp', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get attendance report for today
    report = db.get_daily_report(date=today)
    
    return render_template('dashboard.html', report=report)

@app.route('/employees')
def employees():
    # Get all employees
    all_employees = db.get_all_employees()
    return render_template('employees.html', employees=all_employees)

@app.route('/attendance')
def attendance():
    # Get date parameter or use today
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Get attendance records for the date
    attendance_records = db.get_attendance(date=date)
    
    return render_template('attendance.html', attendance_records=attendance_records, selected_date=date)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        employee_id = int(request.form['employee_id'])
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        position = request.form['position']
        join_date = request.form['join_date']
        
        # Add employee to database
        success = db.add_employee(employee_id, name, email, department, position, join_date)
        
        if success:
            # Store employee_id in session for face registration
            session['registering_employee_id'] = employee_id
            session['registering_employee_name'] = name
            return redirect(url_for('register_face'))
        else:
            return render_template('register.html', error="Failed to register employee. ID may already exist.")
    
    return render_template('register.html')

@app.route('/register_face', methods=['GET', 'POST'])
def register_face():
    if 'registering_employee_id' not in session:
        return redirect(url_for('register'))
    
    employee_id = session['registering_employee_id']
    employee_name = session['registering_employee_name']
    
    if request.method == 'POST':
        # Get the captured face images from the form
        face_images = []
        for i in range(5):  # Assuming 5 images are captured
            image_data = request.form.get(f'image_{i}')
            if image_data:
                # Convert base64 image to OpenCV format
                encoded_data = image_data.split(',')[1]
                nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img is not None:
                    face_images.append(img)
        
        if face_images:
            # Register employee faces
            success = face_system.register_employee(employee_id, employee_name, face_images)
            
            if success:
                # Clear session data
                session.pop('registering_employee_id', None)
                session.pop('registering_employee_name', None)
                
                return redirect(url_for('employees', success=f"Successfully registered {employee_name}"))
            else:
                return render_template('register_face.html', 
                                      employee_id=employee_id, 
                                      employee_name=employee_name,
                                      error="Failed to register face. Please try again.")
        else:
            return render_template('register_face.html', 
                                  employee_id=employee_id, 
                                  employee_name=employee_name,
                                  error="No face images captured. Please try again.")
    
    return render_template('register_face.html', 
                          employee_id=employee_id, 
                          employee_name=employee_name)

@app.route('/attendance_kiosk')
def attendance_kiosk():
    return render_template('attendance_kiosk.html')

@app.route('/api/detect_face', methods=['POST'])
def detect_face():
    # Get image data from request
    image_data = request.json.get('image')
    if not image_data:
        return jsonify({'success': False, 'error': 'No image data provided'})
    
    try:
        # Convert base64 image to OpenCV format
        encoded_data = image_data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'success': False, 'error': 'Invalid image data'})
        
        # Detect faces
        faces = face_system.detect_faces(img)
        
        if len(faces) == 0:
            return jsonify({'success': False, 'error': 'No face detected'})
        
        if len(faces) > 1:
            return jsonify({'success': False, 'error': 'Multiple faces detected'})
        
        # Recognize the face
        face_rect = faces[0]
        employee_id, employee_name, confidence = face_system.recognize_face(img, face_rect)
        
        if employee_id == -1:
            return jsonify({'success': False, 'error': 'Face not recognized'})
        
        # Record attendance
        event_type = request.json.get('event_type', 'check_in')
        timestamp = db.record_attendance(employee_id, event_type)
        
        # Get employee details
        employee = db.get_employee(employee_id)
        
        return jsonify({
            'success': True,
            'employee_id': employee_id,
            'employee_name': employee_name,
            'department': employee.get('department', ''),
            'event_type': event_type,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_report', methods=['GET'])
def get_report():
    # Get date parameter or use today
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Get report for the date
    report = db.get_daily_report(date=date)
    
    if report:
        return jsonify({'success': True, 'report': report})
    else:
        return jsonify({'success': False, 'error': 'Failed to generate report'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
