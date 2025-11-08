# Healthcare Portal - Human + AI Interactive System

## Overview
A full-stack healthcare management system that enables seamless communication between patients and doctors, enhanced by AI-powered medical data analysis. Built with Flask (Python backend) and HTML/CSS/JavaScript (frontend).

## Recent Changes
**November 8, 2025**
- Complete implementation of healthcare portal with patient and doctor interfaces
- Integrated OpenAI API for AI-powered medical analysis and health insights
- Database schema created with user authentication, patient data, and doctor notes
- Responsive design with professional healthcare theme
- File upload system for medical documents

## Project Architecture

### Backend (Flask)
- **app.py**: Main Flask application with routes for authentication, patient portal, and doctor dashboard
- **init_db.py**: Database initialization script with schema and demo users
- **database.db**: SQLite database storing users, patient data, and doctor notes

### Frontend
- **templates/**: HTML templates for all pages
  - `index.html`: Login page with separate patient/doctor authentication
  - `patient_portal.html`: Patient interface for submitting health data
  - `doctor_dashboard.html`: Doctor interface for viewing patient data and AI insights
- **static/css/style.css**: Professional healthcare theme with responsive design
- **static/js/main.js**: Client-side validation and modal interactions

### AI Integration
- Uses OpenAI API (GPT-3.5-turbo) for analyzing patient symptoms and medical history
- Generates health priority levels (High/Medium/Low)
- Provides AI summaries for doctors to review

### Database Schema
1. **users**: Stores user credentials (username, password, role, full_name, email)
2. **patient_data**: Patient health records with symptoms, medical history, and AI analysis
3. **doctor_notes**: Clinical notes added by doctors for patient records

## Key Features
1. **Role-Based Authentication**: Separate login flows for patients and doctors
2. **Patient Portal**: 
   - Submit health information (age, gender, symptoms, medical history, medications)
   - Upload medical files (PDF, images, documents)
   - View submission history with AI-generated insights
3. **Doctor Dashboard**:
   - View all patient reports with priority levels
   - Access AI-generated analysis and health summaries
   - Add clinical notes to patient records
   - Statistics overview (total reports, priority breakdown)
4. **AI Analysis**: Automated analysis of patient data to assist doctors
5. **File Management**: Secure file upload and storage system

## Demo Credentials
### Patients
- Username: `patient1` | Password: `patient123`
- Username: `patient2` | Password: `patient123`

### Doctors
- Username: `doctor1` | Password: `doctor123`
- Username: `doctor2` | Password: `doctor123`

## Environment Variables
- `SESSION_SECRET`: Flask session secret key (configured)
- `OPENAI_API_KEY`: Required for AI analysis features (ask user to add)

## Workflow
- **Flask Healthcare App**: Runs the Flask development server on port 5000
  - Command: `python app.py`
  - Accessible at the webview URL

## Dependencies
- flask
- flask-session
- werkzeug
- openai
- sqlite3 (built-in)

## Project Structure
```
.
├── app.py                      # Main Flask application
├── init_db.py                  # Database initialization
├── database.db                 # SQLite database
├── templates/
│   ├── index.html             # Login page
│   ├── patient_portal.html    # Patient interface
│   └── doctor_dashboard.html  # Doctor interface
├── static/
│   ├── css/
│   │   └── style.css          # Styling
│   ├── js/
│   │   └── main.js            # Client-side scripts
│   └── uploads/               # Medical file storage
└── replit.md                  # This file
```

## Next Steps / Future Enhancements
- Add appointment scheduling system
- Implement secure messaging between patients and doctors
- Create medical history timeline visualization
- Add PDF export for medical reports
- Implement role-based admin dashboard
- Add email notifications for new reports
- Enhance AI analysis with medical knowledge base
- Add patient-doctor chat functionality
