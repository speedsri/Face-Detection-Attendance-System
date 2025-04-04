#!/bin/bash

# Test script for Face Attendance System
# This script tests the integration of frontend and backend components

echo "Running integration tests for Face Attendance System..."

# Check if required directories exist
echo "Checking directory structure..."
directories=("data" "data/employees" "data/temp" "static" "static/images" "static/css" "static/js" "templates" "src")
for dir in "${directories[@]}"; do
  if [ -d "$dir" ]; then
    echo "✓ Directory $dir exists"
  else
    echo "✗ Directory $dir is missing"
    exit 1
  fi
done

# Check if required files exist
echo "Checking core files..."
files=("src/app.py" "src/database.py" "src/face_detection.py" "templates/index.html" "templates/dashboard.html" 
       "templates/employees.html" "templates/attendance.html" "templates/register.html" "templates/register_face.html" 
       "templates/attendance_kiosk.html" "static/images/default-avatar.png" "static/css/custom.css" "init.sh")
for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ File $file exists"
  else
    echo "✗ File $file is missing"
    exit 1
  fi
done

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import cv2" 2>/dev/null
if [ $? -eq 0 ]; then
  echo "✓ OpenCV is installed"
else
  echo "✗ OpenCV is not installed"
fi

python3 -c "import flask" 2>/dev/null
if [ $? -eq 0 ]; then
  echo "✓ Flask is installed"
else
  echo "✗ Flask is not installed"
  echo "Installing Flask..."
  pip3 install flask
fi

# Test database initialization
echo "Testing database initialization..."
python3 -c "from src.database import EmployeeDatabase; db = EmployeeDatabase(); print('Database initialized successfully')"
if [ $? -eq 0 ]; then
  echo "✓ Database initialization successful"
else
  echo "✗ Database initialization failed"
  exit 1
fi

# Test face detection module
echo "Testing face detection module..."
python3 -c "from src.face_detection import FaceDetectionSystem; face_system = FaceDetectionSystem(); print('Face detection system initialized successfully')"
if [ $? -eq 0 ]; then
  echo "✓ Face detection module initialization successful"
else
  echo "✗ Face detection module initialization failed"
  exit 1
fi

echo "All integration tests passed successfully!"
echo "The system is ready for deployment."
