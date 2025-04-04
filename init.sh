
#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install flask opencv-python numpy

# Initialize database
mkdir -p data
python3 src/database.py

# Create default avatar
python3 create_default_avatar.py

# Start the application
echo "Starting Face Attendance System..."
python3 src/app.py
