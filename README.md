# 🔍 Face Detection Attendance System

<div align="center">
  
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8+-orange.svg?style=for-the-badge)

</div>

<div align="center">
  <h3>A modern, contactless attendance tracking solution powered by facial recognition</h3>
</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Working Principles](#-working-principles)
- [Installation Guide](#-installation-guide)
- [System Requirements](#-system-requirements)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Directory Structure](#-directory-structure)
- [Support](#-support)

---

## 🌟 Overview

The Face Detection Attendance System provides an automated solution for tracking employee attendance using cutting-edge facial recognition technology. This system delivers a contactless, efficient way to record employee check-ins and check-outs, eliminating the need for traditional methods like ID cards or biometric fingerprint scanners.

---

## ✨ Features

<table>
  <tr>
    <td width="50%">
      <h3>🧠 Facial Recognition</h3>
      <p>Automatically identifies employees through their unique facial features</p>
    </td>
    <td width="50%">
      <h3>⏱️ Real-time Tracking</h3>
      <p>Records check-in and check-out times instantly with time stamps</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>👥 Employee Management</h3>
      <p>Easy registration and management of employee profiles</p>
    </td>
    <td width="50%">
      <h3>📊 Reporting</h3>
      <p>Comprehensive attendance reports and analytics</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🖥️ User-friendly Interface</h3>
      <p>Intuitive web-based interface for all users</p>
    </td>
    <td width="50%">
      <h3>🔒 Secure Database</h3>
      <p>Reliable storage of employee data and attendance records</p>
    </td>
  </tr>
</table>

---

## 🔍 Working Principles

The Face Detection Attendance System operates on the following core principles:

### 1. Face Detection & Recognition Process

```mermaid
graph LR
    A[Camera Input] --> B[Face Detection]
    B --> C[Face Alignment]
    C --> D[Feature Extraction]
    D --> E[Face Recognition]
    E --> F[Database Matching]
    F --> G[Attendance Logging]
    style A fill:#d0e1f9,stroke:#3498db
    style B fill:#d0e1f9,stroke:#3498db
    style C fill:#d0e1f9,stroke:#3498db
    style D fill:#d0e1f9,stroke:#3498db
    style E fill:#d0e1f9,stroke:#3498db
    style F fill:#d0e1f9,stroke:#3498db
    style G fill:#d0e1f9,stroke:#3498db
```

### 2. Technical Implementation

The system leverages advanced computer vision techniques to:

- **Detect faces** in real-time camera feed using Haar Cascade Classifiers or Deep Neural Networks
- **Extract facial features** and create unique face embeddings using techniques such as OpenCV
- **Match detected faces** against the database of registered employees
- **Record attendance** with precise timestamps when a match is found
- **Generate reports** based on the accumulated attendance data

### 3. Security Measures

- Facial data is stored as encrypted mathematical representations, not actual images
- Role-based access controls for system administrators and users
- Secure database with regular backup procedures
- Audit logging for all system activities

---

## 💻 Installation Guide

### 🔧 System Requirements

| Requirement | Specification |
|-------------|---------------|
| **Operating System** | Ubuntu 20.04+ / Windows 10+ / macOS 10.15+ |
| **Python** | Version 3.8 or higher |
| **Hardware** | Webcam required for face detection |
| **Storage** | Minimum 1GB free space |
| **Memory** | Minimum 4GB RAM |

### 🚀 Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/face-detection-attendance.git
cd face-detection-attendance
```

#### 2. Setup Environment

##### For Linux/macOS:

```bash
# Make the initialization script executable
chmod +x init.sh

# Run the initialization script
./init.sh
```

##### For Windows:

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
```

#### 3. Launch the Application

```bash
# Start the application
python src/app.py
```

#### 4. Access the Web Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

---

## 📱 Usage

### Admin Portal

1. Log in with administrator credentials
2. Register new employees by capturing their facial data
3. View attendance reports and analytics
4. Manage user roles and permissions

### Employee Use

1. Stand in front of the camera
2. The system automatically detects and recognizes the face
3. Attendance is logged with timestamp
4. Employee can view their own attendance history

---

## 📁 Directory Structure

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

---

## 🆘 Support

For support, please contact:
- 📧 Email: earsekanayake@yandex.com
- ☎️ Phone:+94 (071) 803-2779

---

<div align="center">
  <p>© 2025 Face Attendance System. All rights reserved.</p>
  <p>Made with ❤️ for efficient workplace management</p>
</div>
