# README.md - Face Detection Attendance System

## Overview

The Face Detection Attendance System is an automated solution for tracking employee attendance using facial recognition technology. This system provides a contactless, efficient way to record employee check-ins and check-outs, eliminating the need for traditional methods like ID cards or biometric fingerprint scanners.

## Key Features

- **Facial Recognition**: Automatically identifies employees through their facial features
- **Real-time Attendance Tracking**: Records check-in and check-out times instantly
- **Employee Management**: Easy registration and management of employee profiles
- **Reporting**: Comprehensive attendance reports and analytics
- **User-friendly Interface**: Intuitive web-based interface for both employees and administrators
- **Secure Database**: Reliable storage of employee data and attendance records

## System Requirements

- **Operating System**: Ubuntu 20.04+ / Windows 10+ / macOS 10.15+
- **Python**: Version 3.8 or higher
- **Webcam**: Required for face detection
- **Storage**: Minimum 1GB free space
- **Memory**: Minimum 4GB RAM

## Quick Start

1. **Clone or download the repository**

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

## Documentation

For detailed information, please refer to the following documentation:

- [Complete Documentation](docs/documentation.md)
- [Implementation Guide](docs/implementation_guide.md)
- [User Guide](docs/user_guide.md)

## Directory Structure

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
├── docs/                  # Documentation
├── create_default_avatar.py # Script to create default avatar
├── init.sh                # Initialization script
└── README.md              # Project readme
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact:
- Email: support@faceattendance.com
- Phone: (123) 456-7890

---

© 2025 Face Attendance System. All rights reserved.
