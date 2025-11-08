import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            age INTEGER,
            gender TEXT,
            symptoms TEXT,
            medical_history TEXT,
            current_medications TEXT,
            file_path TEXT,
            file_name TEXT,
            ai_analysis TEXT,
            health_priority TEXT,
            ai_summary TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctor_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_data_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            notes TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_data_id) REFERENCES patient_data (id),
            FOREIGN KEY (doctor_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='patient'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, role, full_name, email)
            VALUES 
            (?, ?, ?, ?, ?),
            (?, ?, ?, ?, ?),
            (?, ?, ?, ?, ?),
            (?, ?, ?, ?, ?)
        ''', (
            'patient1', generate_password_hash('patient123'), 'patient', 'John Doe', 'john.doe@example.com',
            'patient2', generate_password_hash('patient123'), 'patient', 'Jane Smith', 'jane.smith@example.com',
            'doctor1', generate_password_hash('doctor123'), 'doctor', 'Dr. Sarah Johnson', 'sarah.johnson@hospital.com',
            'doctor2', generate_password_hash('doctor123'), 'doctor', 'Dr. Michael Chen', 'michael.chen@hospital.com'
        ))
        print("Demo users created:")
        print("Patients: patient1/patient123, patient2/patient123")
        print("Doctors: doctor1/doctor123, doctor2/doctor123")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
