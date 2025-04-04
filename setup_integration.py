import os
import shutil
from datetime import datetime

# Create necessary directories
os.makedirs('data', exist_ok=True)
os.makedirs('data/employees', exist_ok=True)
os.makedirs('data/temp', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

# Create a CSS file for custom styles
css_content = """
/* Custom styles for Face Attendance System */
.hero-section {
    background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/static/images/hero-bg.jpg');
    background-size: cover;
    background-position: center;
}

.employee-img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #0d6efd;
}

.stat-card {
    text-align: center;
    padding: 20px;
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
}
"""

# Write CSS file
with open('static/css/custom.css', 'w') as f:
    f.write(css_content)

# Create a placeholder hero background image
try:
    # If the default avatar was created, copy and modify it for the hero background
    if os.path.exists('static/images/default-avatar.png'):
        shutil.copy('static/images/default-avatar.png', 'static/images/hero-bg.jpg')
        print("Created hero background image")
    else:
        print("Default avatar not found, skipping hero background creation")
except Exception as e:
    print(f"Error creating hero background: {e}")

# Create an initialization script
init_script = """
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
"""

# Write initialization script
with open('init.sh', 'w') as f:
    f.write(init_script)

# Make the script executable
os.chmod('init.sh', 0o755)

print("Integration setup completed successfully!")
print(f"Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
