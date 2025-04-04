# Face Detection Attendance System - Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Installation Guide](#installation-guide)
4. [User Manual](#user-manual)
5. [Administrator Guide](#administrator-guide)
6. [Technical Documentation](#technical-documentation)
7. [Troubleshooting](#troubleshooting)

## Introduction

The Face Detection Attendance System is an automated solution for tracking employee attendance using facial recognition technology. This system provides a contactless, efficient way to record employee check-ins and check-outs, eliminating the need for traditional methods like ID cards or biometric fingerprint scanners.

### Key Features

- **Facial Recognition**: Automatically identifies employees through their facial features
- **Real-time Attendance Tracking**: Records check-in and check-out times instantly
- **Employee Management**: Easy registration and management of employee profiles
- **Reporting**: Comprehensive attendance reports and analytics
- **User-friendly Interface**: Intuitive web-based interface for both employees and administrators
- **Secure Database**: Reliable storage of employee data and attendance records

## System Overview

The Face Detection Attendance System consists of the following components:

1. **Face Detection Module**: Uses OpenCV to detect and recognize employee faces
2. **Database System**: SQLite database for storing employee information and attendance records
3. **Web Interface**: Flask-based web application with HTML/CSS/JS frontend
4. **Attendance Kiosk**: Camera interface for employee check-in/check-out

### System Architecture

The system follows a client-server architecture:

- **Backend**: Python-based server using Flask framework
- **Frontend**: HTML/CSS/JavaScript web interface
- **Database**: SQLite for data storage
- **Computer Vision**: OpenCV for face detection and recognition

## Installation Guide

### System Requirements

- **Operating System**: Ubuntu 20.04+ / Windows 10+ / macOS 10.15+
- **Python**: Version 3.8 or higher
- **Webcam**: Required for face detection
- **Storage**: Minimum 1GB free space
- **Memory**: Minimum 4GB RAM

### Installation Steps

1. **Clone or download the repository**

   ```bash
   git clone https://github.com/yourusername/face-attendance-system.git
   cd face-attendance-system
   ```

2. **Run the initialization script**

   ```bash
   # Make the script executable (Linux/macOS)
   chmod +x init.sh
   
   # Run the script
   ./init.sh
   ```

   For Windows:
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   venv\Scripts\activate
   
   # Install required packages
   pip install flask opencv-python numpy
   
   # Initialize the database
   python src/database.py
   
   # Create default avatar
   python create_default_avatar.py
   
   # Start the application
   python src/app.py
   ```

3. **Access the web interface**

   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## User Manual

### Employee Registration

1. Navigate to the "Employees" page
2. Click on "Add New Employee"
3. Fill in the required information (ID, name, department, etc.)
4. Click "Continue to Face Registration"
5. Follow the on-screen instructions to capture face images
6. Click "Complete Registration" when finished

### Using the Attendance Kiosk

1. Navigate to the "Attendance Kiosk" page
2. Position your face in front of the camera
3. Click either "Check In" or "Check Out" button
4. Wait for the confirmation message

### Viewing Attendance Records

1. Navigate to the "Attendance" page
2. Use the date selector to choose a specific date
3. View your attendance records for the selected date

## Administrator Guide

### System Administration

1. **Managing Employees**
   - Add, edit, or remove employee profiles
   - View employee details and attendance history

2. **Generating Reports**
   - Access the "Dashboard" for attendance overview
   - Generate daily, weekly, or monthly reports
   - Export reports in CSV format

3. **System Configuration**
   - Adjust face recognition sensitivity
   - Configure working hours and attendance rules
   - Manage user permissions

### Database Management

The system uses SQLite for data storage. The database file is located at:
```
data/attendance.db
```

To backup the database:
```bash
cp data/attendance.db data/attendance_backup_$(date +%Y%m%d).db
```

## Technical Documentation

### Directory Structure

```
face_attendance_system/
├── data/                  # Data storage directory
│   ├── employees/         # Employee face data
│   └── attendance.db      # SQLite database
├── src/                   # Source code
│   ├── app.py             # Flask application
│   ├── database.py        # Database operations
│   └── face_detection.py  # Face detection module
├── static/                # Static files
│   ├── css/               # CSS stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Image assets
├── templates/             # HTML templates
├── create_default_avatar.py # Script to create default avatar
├── init.sh                # Initialization script
└── README.md              # Project readme
```

### Face Detection Module

The face detection module uses OpenCV for face detection and a custom feature extraction approach for face recognition. The system:

1. Detects faces using Haar Cascade Classifier
2. Extracts features using histogram-based approach
3. Compares features with stored employee data
4. Identifies the employee based on feature similarity

### Database Schema

The system uses three main tables:

1. **employees**: Stores employee information
   - id (PRIMARY KEY)
   - name
   - email
   - department
   - position
   - join_date
   - created_at

2. **attendance**: Records attendance events
   - id (PRIMARY KEY)
   - employee_id (FOREIGN KEY)
   - event_type (check_in/check_out)
   - timestamp
   - date

3. **face_data**: Stores face image references
   - id (PRIMARY KEY)
   - employee_id (FOREIGN KEY)
   - face_file_path
   - created_at

### API Endpoints

The system provides the following API endpoints:

- `/api/detect_face`: Detects and recognizes faces from image data
- `/api/get_report`: Generates attendance reports for a specific date

## Troubleshooting

### Common Issues

1. **Face not recognized**
   - Ensure proper lighting conditions
   - Try registering additional face images from different angles
   - Adjust your position in front of the camera

2. **System not starting**
   - Check if all dependencies are installed
   - Verify Python version (3.8+)
   - Ensure webcam is properly connected and accessible

3. **Database errors**
   - Check file permissions for the database file
   - Ensure the data directory exists and is writable

### Support

For additional support, please contact:
- Email: support@faceattendance.com
- Phone: (123) 456-7890

---

© 2025 Face Attendance System. All rights reserved.
