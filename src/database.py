import sqlite3
import os
from datetime import datetime

class EmployeeDatabase:
    def __init__(self, db_path='data/attendance.db'):
        """
        Initialize the employee database
        
        Args:
            db_path: Path to the SQLite database file
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Initialize the database
        self._connect()
        self._create_tables()
        self._disconnect()
    
    def _connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def _disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        # Employees table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            department TEXT,
            position TEXT,
            join_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Attendance table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
        ''')
        
        # Face data table (to store face encoding references)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            face_file_path TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
        ''')
        
        self.conn.commit()
    
    def add_employee(self, employee_id, name, email=None, department=None, position=None, join_date=None):
        """
        Add a new employee to the database
        
        Args:
            employee_id: Unique ID for the employee
            name: Name of the employee
            email: Email address of the employee
            department: Department of the employee
            position: Position/role of the employee
            join_date: Date when the employee joined
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._connect()
            
            # Check if employee already exists
            self.cursor.execute("SELECT id FROM employees WHERE id = ?", (employee_id,))
            if self.cursor.fetchone():
                print(f"Employee with ID {employee_id} already exists")
                return False
            
            # Add employee
            self.cursor.execute(
                "INSERT INTO employees (id, name, email, department, position, join_date) VALUES (?, ?, ?, ?, ?, ?)",
                (employee_id, name, email, department, position, join_date)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False
        finally:
            self._disconnect()
    
    def update_employee(self, employee_id, name=None, email=None, department=None, position=None):
        """
        Update employee information
        
        Args:
            employee_id: ID of the employee to update
            name: New name (or None to keep current)
            email: New email (or None to keep current)
            department: New department (or None to keep current)
            position: New position (or None to keep current)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._connect()
            
            # Check if employee exists
            self.cursor.execute("SELECT id FROM employees WHERE id = ?", (employee_id,))
            if not self.cursor.fetchone():
                print(f"Employee with ID {employee_id} does not exist")
                return False
            
            # Build update query dynamically based on provided fields
            update_fields = []
            params = []
            
            if name is not None:
                update_fields.append("name = ?")
                params.append(name)
            
            if email is not None:
                update_fields.append("email = ?")
                params.append(email)
            
            if department is not None:
                update_fields.append("department = ?")
                params.append(department)
            
            if position is not None:
                update_fields.append("position = ?")
                params.append(position)
            
            if not update_fields:
                print("No fields to update")
                return False
            
            # Add employee_id to params
            params.append(employee_id)
            
            # Execute update
            query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = ?"
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating employee: {e}")
            return False
        finally:
            self._disconnect()
    
    def delete_employee(self, employee_id):
        """
        Delete an employee from the database
        
        Args:
            employee_id: ID of the employee to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._connect()
            
            # Check if employee exists
            self.cursor.execute("SELECT id FROM employees WHERE id = ?", (employee_id,))
            if not self.cursor.fetchone():
                print(f"Employee with ID {employee_id} does not exist")
                return False
            
            # Delete employee's face data
            self.cursor.execute("DELETE FROM face_data WHERE employee_id = ?", (employee_id,))
            
            # Delete employee's attendance records
            self.cursor.execute("DELETE FROM attendance WHERE employee_id = ?", (employee_id,))
            
            # Delete employee
            self.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False
        finally:
            self._disconnect()
    
    def get_employee(self, employee_id):
        """
        Get employee information
        
        Args:
            employee_id: ID of the employee
            
        Returns:
            Dictionary with employee information or None if not found
        """
        try:
            self._connect()
            
            self.cursor.execute(
                "SELECT id, name, email, department, position, join_date FROM employees WHERE id = ?", 
                (employee_id,)
            )
            
            employee = self.cursor.fetchone()
            if employee:
                return {
                    'id': employee[0],
                    'name': employee[1],
                    'email': employee[2],
                    'department': employee[3],
                    'position': employee[4],
                    'join_date': employee[5]
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting employee: {e}")
            return None
        finally:
            self._disconnect()
    
    def get_all_employees(self):
        """
        Get all employees
        
        Returns:
            List of dictionaries with employee information
        """
        try:
            self._connect()
            
            self.cursor.execute(
                "SELECT id, name, email, department, position, join_date FROM employees ORDER BY name"
            )
            
            employees = []
            for row in self.cursor.fetchall():
                employees.append({
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'department': row[3],
                    'position': row[4],
                    'join_date': row[5]
                })
            
            return employees
        except Exception as e:
            print(f"Error getting employees: {e}")
            return []
        finally:
            self._disconnect()
    
    def add_face_data(self, employee_id, face_file_path):
        """
        Add face data for an employee
        
        Args:
            employee_id: ID of the employee
            face_file_path: Path to the face image file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._connect()
            
            # Check if employee exists
            self.cursor.execute("SELECT id FROM employees WHERE id = ?", (employee_id,))
            if not self.cursor.fetchone():
                print(f"Employee with ID {employee_id} does not exist")
                return False
            
            # Add face data
            self.cursor.execute(
                "INSERT INTO face_data (employee_id, face_file_path) VALUES (?, ?)",
                (employee_id, face_file_path)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding face data: {e}")
            return False
        finally:
            self._disconnect()
    
    def get_face_data(self, employee_id):
        """
        Get face data for an employee
        
        Args:
            employee_id: ID of the employee
            
        Returns:
            List of face file paths
        """
        try:
            self._connect()
            
            self.cursor.execute(
                "SELECT face_file_path FROM face_data WHERE employee_id = ?", 
                (employee_id,)
            )
            
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting face data: {e}")
            return []
        finally:
            self._disconnect()
    
    def record_attendance(self, employee_id, event_type='check_in'):
        """
        Record attendance for an employee
        
        Args:
            employee_id: ID of the employee
            event_type: Type of event ('check_in' or 'check_out')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._connect()
            
            # Check if employee exists
            self.cursor.execute("SELECT id FROM employees WHERE id = ?", (employee_id,))
            if not self.cursor.fetchone():
                print(f"Employee with ID {employee_id} does not exist")
                return False
            
            # Get current timestamp and date
            now = datetime.now()
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            date = now.strftime('%Y-%m-%d')
            
            # Record attendance
            self.cursor.execute(
                "INSERT INTO attendance (employee_id, event_type, timestamp, date) VALUES (?, ?, ?, ?)",
                (employee_id, event_type, timestamp, date)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error recording attendance: {e}")
            return False
        finally:
            self._disconnect()
    
    def get_attendance(self, date=None, employee_id=None):
        """
        Get attendance records
        
        Args:
            date: Date string in format 'YYYY-MM-DD', or None for all dates
            employee_id: ID of the employee, or None for all employees
            
        Returns:
            List of attendance records
        """
        try:
            self._connect()
            
            query = """
                SELECT a.id, a.employee_id, e.name, a.event_type, a.timestamp, a.date
                FROM attendance a
                JOIN employees e ON a.employee_id = e.id
                WHERE 1=1
            """
            params = []
            
            if date:
                query += " AND a.date = ?"
                params.append(date)
            
            if employee_id:
                query += " AND a.employee_id = ?"
                params.append(employee_id)
            
            query += " ORDER BY a.timestamp"
            
            self.cursor.execute(query, params)
            
            attendance_records = []
            for row in self.cursor.fetchall():
                attendance_records.append({
                    'id': row[0],
                    'employee_id': row[1],
                    'employee_name': row[2],
                    'event_type': row[3],
                    'timestamp': row[4],
                    'date': row[5]
                })
            
            return attendance_records
        except Exception as e:
            print(f"Error getting attendance: {e}")
            return []
        finally:
            self._disconnect()
    
    def get_daily_report(self, date=None):
        """
        Get daily attendance report
        
        Args:
            date: Date string in format 'YYYY-MM-DD', or None for today
            
        Returns:
            Dictionary with employee attendance summary
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            self._connect()
            
            # Get all employees
            employees = self.get_all_employees()
            
            report = {
                'date': date,
                'total_employees': len(employees),
                'present': 0,
                'absent': 0,
                'employee_records': []
            }
            
            # Get attendance for the date
            attendance = self.get_attendance(date=date)
            
            # Group attendance by employee
            attendance_by_employee = {}
            for record in attendance:
                employee_id = record['employee_id']
                if employee_id not in attendance_by_employee:
                    attendance_by_employee[employee_id] = []
                attendance_by_employee[employee_id].append(record)
            
            # Process each employee
            for employee in employees:
                employee_id = employee['id']
                employee_record = {
                    'id': employee_id,
                    'name': employee['name'],
                    'department': employee['department'],
                    'status': 'Absent',
                    'check_in': None,
                    'check_out': None
                }
                
                if employee_id in attendance_by_employee:
                    employee_record['status'] = 'Present'
                    report['present'] += 1
                    
                    # Find check-in and check-out times
                    for record in attendance_by_employee[employee_id]:
                        if record['event_type'] == 'check_in' and (employee_record['check_in'] is None or record['timestamp'] < employee_record['check_in']):
                            employee_record['check_in'] = record['timestamp']
                        elif record['event_type'] == 'check_out' and (employee_record['check_out'] is None or record['timestamp'] > employee_record['check_out']):
                            employee_record['check_out'] = record['timestamp']
                else:
                    report['absent'] += 1
                
                report['employee_records'].append(employee_record)
            
            return report
        except Exception as e:
            print(f"Error generating daily report: {e}")
            return None
        finally:
            self._disconnect()


# Example usage
if __name__ == "__main__":
    # Initialize the database
    db = EmployeeDatabase()
    
    # Add some test employees
    db.add_employee(1, "John Doe", "john.doe@example.com", "IT", "Developer", "2023-01-15")
    db.add_employee(2, "Jane Smith", "jane.smith@example.com", "HR", "Manager", "2022-05-10")
    
    # Record attendance
    db.record_attendance(1, "check_in")
    db.record_attendance(2, "check_in")
    
    # Get all employees
    employees = db.get_all_employees()
    print("All Employees:")
    for employee in employees:
        print(f"ID: {employee['id']}, Name: {employee['name']}, Department: {employee['department']}")
    
    # Get attendance for today
    today = datetime.now().strftime('%Y-%m-%d')
    attendance = db.get_attendance(date=today)
    print(f"\nAttendance for {today}:")
    for record in attendance:
        print(f"Employee: {record['employee_name']}, Event: {record['event_type']}, Time: {record['timestamp']}")
    
    # Generate daily report
    report = db.get_daily_report()
    print(f"\nDaily Report for {report['date']}:")
    print(f"Total Employees: {report['total_employees']}")
    print(f"Present: {report['present']}")
    print(f"Absent: {report['absent']}")
    print("\nEmployee Records:")
    for record in report['employee_records']:
        print(f"Name: {record['name']}, Status: {record['status']}, Check-in: {record['check_in']}, Check-out: {record['check_out']}")
