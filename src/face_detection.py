import cv2
import numpy as np
import os
import time
import pickle
from datetime import datetime

class FaceDetectionSystem:
    def __init__(self, cascade_path=None, employee_data_path='data/employees'):
        """
        Initialize the face detection system
        
        Args:
            cascade_path: Path to the Haar cascade XML file for face detection
            employee_data_path: Path to the directory containing employee face data
        """
        # Use default cascade if none provided
        if cascade_path is None:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        else:
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
        self.employee_data_path = employee_data_path
        self.known_faces = {}
        self.face_features = {}
        
        # Create employee data directory if it doesn't exist
        os.makedirs(self.employee_data_path, exist_ok=True)
        
        # Try to load existing face recognition data if available
        model_path = os.path.join(self.employee_data_path, 'face_features.pkl')
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.face_features = data.get('features', {})
                    self.known_faces = data.get('names', {})
                print("Loaded existing face recognition data")
            except Exception as e:
                print(f"Error loading face data: {e}")
                self._load_employee_data()
        else:
            self._load_employee_data()
    
    def _load_employee_data(self):
        """Load employee data from the employee data directory"""
        employee_info_path = os.path.join(self.employee_data_path, 'employee_info.txt')
        if os.path.exists(employee_info_path):
            with open(employee_info_path, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        employee_id = int(parts[0])
                        employee_name = parts[1]
                        self.known_faces[employee_id] = employee_name
        
        # Load face features for each employee
        self._load_face_features()
    
    def _load_face_features(self):
        """Load face features for each employee"""
        self.face_features = {}
        
        # Check if there are any employee directories
        if not os.path.exists(self.employee_data_path):
            print("No employee data found. Please register employees first.")
            return
        
        employee_dirs = [d for d in os.listdir(self.employee_data_path) 
                        if os.path.isdir(os.path.join(self.employee_data_path, d)) and d.isdigit()]
        
        if not employee_dirs:
            print("No employee data found. Please register employees first.")
            return
        
        # Load face images for each employee
        for employee_dir in employee_dirs:
            employee_id = int(employee_dir)
            employee_path = os.path.join(self.employee_data_path, employee_dir)
            
            # Get employee name from info file
            info_file = os.path.join(employee_path, 'info.txt')
            if os.path.exists(info_file):
                with open(info_file, 'r') as f:
                    employee_name = f.read().strip()
                    self.known_faces[employee_id] = employee_name
            else:
                self.known_faces[employee_id] = f"Employee {employee_id}"
            
            # Load face images and extract features
            face_images = [f for f in os.listdir(employee_path) if f.endswith('.jpg') or f.endswith('.png')]
            if face_images:
                employee_features = []
                for face_file in face_images:
                    face_path = os.path.join(employee_path, face_file)
                    face_img = cv2.imread(face_path)
                    if face_img is not None:
                        # Extract simple features (histogram-based)
                        features = self._extract_features(face_img)
                        if features is not None:
                            employee_features.append(features)
                
                if employee_features:
                    # Store average features for the employee
                    self.face_features[employee_id] = np.mean(employee_features, axis=0)
        
        # Save the features
        if self.face_features:
            self._save_face_features()
            print(f"Loaded face features for {len(self.face_features)} employees")
        else:
            print("No face features found")
    
    def _extract_features(self, image):
        """
        Extract simple features from a face image
        
        Args:
            image: Input face image (BGR format)
            
        Returns:
            Feature vector
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Resize to standard size
            resized = cv2.resize(gray, (100, 100))
            
            # Compute histogram features
            hist = cv2.calcHist([resized], [0], None, [64], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            
            # Add some pixel intensity features
            regions = [
                resized[0:50, 0:50],    # Top-left
                resized[0:50, 50:100],  # Top-right
                resized[50:100, 0:50],  # Bottom-left
                resized[50:100, 50:100] # Bottom-right
            ]
            region_means = [np.mean(region) for region in regions]
            
            # Combine features
            features = np.concatenate([hist, np.array(region_means)])
            return features
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def _save_face_features(self):
        """Save face features and employee names"""
        data = {
            'features': self.face_features,
            'names': self.known_faces
        }
        model_path = os.path.join(self.employee_data_path, 'face_features.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(data, f)
        
        # Also save employee info in text format
        employee_info_path = os.path.join(self.employee_data_path, 'employee_info.txt')
        with open(employee_info_path, 'w') as f:
            for employee_id, name in self.known_faces.items():
                f.write(f"{employee_id},{name}\n")
        
        print(f"Saved face features for {len(self.face_features)} employees")
    
    def detect_faces(self, image):
        """
        Detect faces in the given image
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            List of face rectangles (x, y, w, h)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces
    
    def recognize_face(self, image, face_rect):
        """
        Recognize a face in the given image
        
        Args:
            image: Input image (BGR format)
            face_rect: Face rectangle (x, y, w, h)
            
        Returns:
            Tuple of (employee_id, employee_name, confidence)
            If face is not recognized, employee_id will be -1
        """
        if len(self.face_features) == 0:
            return -1, "Unknown", 0
        
        x, y, w, h = face_rect
        face_roi = image[y:y+h, x:x+w]
        
        # Extract features from the face
        features = self._extract_features(face_roi)
        if features is None:
            return -1, "Unknown", 0
        
        # Compare with known faces
        best_match_id = -1
        best_match_score = float('inf')
        
        for employee_id, employee_features in self.face_features.items():
            # Calculate Euclidean distance as similarity score
            score = np.linalg.norm(features - employee_features)
            
            if score < best_match_score:
                best_match_score = score
                best_match_id = employee_id
        
        # Convert score to confidence (lower is better)
        # Normalize to a scale similar to the original implementation
        confidence = best_match_score * 10
        
        # Threshold for recognition
        if confidence < 70:
            employee_name = self.known_faces.get(best_match_id, f"Employee {best_match_id}")
            return best_match_id, employee_name, confidence
        else:
            return -1, "Unknown", confidence
    
    def register_employee(self, employee_id, employee_name, face_images):
        """
        Register a new employee with face images
        
        Args:
            employee_id: Unique ID for the employee
            employee_name: Name of the employee
            face_images: List of face images (BGR format)
            
        Returns:
            True if registration was successful, False otherwise
        """
        if not face_images:
            print("No face images provided for registration")
            return False
        
        # Create directory for employee
        employee_dir = os.path.join(self.employee_data_path, str(employee_id))
        os.makedirs(employee_dir, exist_ok=True)
        
        # Save employee info
        with open(os.path.join(employee_dir, 'info.txt'), 'w') as f:
            f.write(employee_name)
        
        # Save face images and extract features
        employee_features = []
        for i, image in enumerate(face_images):
            face_rects = self.detect_faces(image)
            if len(face_rects) == 1:
                x, y, w, h = face_rects[0]
                face_roi = image[y:y+h, x:x+w]
                face_path = os.path.join(employee_dir, f"face_{i}.jpg")
                cv2.imwrite(face_path, face_roi)
                
                # Extract features
                features = self._extract_features(face_roi)
                if features is not None:
                    employee_features.append(features)
            else:
                print(f"Image {i} has {len(face_rects)} faces detected, skipping")
        
        if employee_features:
            # Store average features for the employee
            self.face_features[employee_id] = np.mean(employee_features, axis=0)
            self.known_faces[employee_id] = employee_name
            
            # Save the updated features
            self._save_face_features()
            return True
        else:
            print("No valid face features could be extracted")
            return False
    
    def record_attendance(self, employee_id, event_type='check_in'):
        """
        Record attendance for an employee
        
        Args:
            employee_id: ID of the employee
            event_type: Type of event ('check_in' or 'check_out')
            
        Returns:
            Timestamp of the recorded attendance
        """
        timestamp = datetime.now()
        attendance_dir = os.path.join(self.employee_data_path, 'attendance')
        os.makedirs(attendance_dir, exist_ok=True)
        
        # Get current date for the attendance file
        date_str = timestamp.strftime('%Y-%m-%d')
        attendance_file = os.path.join(attendance_dir, f"{date_str}.csv")
        
        # Check if file exists, create with header if not
        file_exists = os.path.exists(attendance_file)
        with open(attendance_file, 'a') as f:
            if not file_exists:
                f.write("employee_id,employee_name,event_type,timestamp\n")
            
            employee_name = self.known_faces.get(employee_id, f"Employee {employee_id}")
            time_str = timestamp.strftime('%H:%M:%S')
            f.write(f"{employee_id},{employee_name},{event_type},{time_str}\n")
        
        return timestamp
    
    def get_attendance_report(self, date=None):
        """
        Get attendance report for a specific date
        
        Args:
            date: Date string in format 'YYYY-MM-DD', or None for today
            
        Returns:
            List of attendance records
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        attendance_file = os.path.join(self.employee_data_path, 'attendance', f"{date}.csv")
        if not os.path.exists(attendance_file):
            return []
        
        attendance_records = []
        with open(attendance_file, 'r') as f:
            lines = f.readlines()
            # Skip header
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    record = {
                        'employee_id': int(parts[0]),
                        'employee_name': parts[1],
                        'event_type': parts[2],
                        'timestamp': parts[3]
                    }
                    attendance_records.append(record)
        
        return attendance_records


# Example usage
if __name__ == "__main__":
    # Initialize the face detection system
    face_system = FaceDetectionSystem()
    
    # Capture video from webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        exit()
    
    print("Press 'r' to register a new employee")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        
        # Detect faces
        faces = face_system.detect_faces(frame)
        
        # Draw rectangles around faces and recognize them
        for (x, y, w, h) in faces:
            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Recognize face
            employee_id, employee_name, confidence = face_system.recognize_face(frame, (x, y, w, h))
            
            # Display name and confidence
            if employee_id != -1:
                text = f"{employee_name} ({confidence:.1f})"
                cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow('Face Detection', frame)
        
        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            # Simple registration example
            employee_id = int(input("Enter employee ID: "))
            employee_name = input("Enter employee name: ")
            
            print("Capturing 5 face images. Look at the camera...")
            face_images = []
            for i in range(5):
                print(f"Capturing image {i+1}/5...")
                time.sleep(1)  # Wait for 1 second
                ret, img = cap.read()
                if ret:
                    face_images.append(img.copy())
            
            if face_system.register_employee(employee_id, employee_name, face_images):
                print(f"Successfully registered {employee_name}")
            else:
                print("Registration failed")
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
