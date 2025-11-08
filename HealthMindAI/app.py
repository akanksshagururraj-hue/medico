from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import sqlite3
import os
from datetime import datetime
from openai import OpenAI

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

Session(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_patient_data_with_ai(patient_data):
    try:
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return {
                'analysis': 'AI analysis unavailable - OpenAI API key not configured',
                'priority': 'Medium',
                'summary': 'Manual review required'
            }
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""As a medical AI assistant, analyze this patient data and provide insights:
        
Age: {patient_data.get('age', 'Not provided')}
Gender: {patient_data.get('gender', 'Not provided')}
Symptoms: {patient_data.get('symptoms', 'Not provided')}
Medical History: {patient_data.get('medical_history', 'Not provided')}
Current Medications: {patient_data.get('current_medications', 'Not provided')}

Please provide:
1. A brief analysis of the patient's condition
2. Health priority level (High/Medium/Low)
3. A concise summary for doctors

Format your response as:
ANALYSIS: [your analysis]
PRIORITY: [High/Medium/Low]
SUMMARY: [brief summary]"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant helping doctors analyze patient data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        result_text = response.choices[0].message.content or ""
        
        analysis = ""
        priority = "Medium"
        summary = ""
        
        for line in result_text.split('\n'):
            if line.startswith('ANALYSIS:'):
                analysis = line.replace('ANALYSIS:', '').strip()
            elif line.startswith('PRIORITY:'):
                priority = line.replace('PRIORITY:', '').strip()
            elif line.startswith('SUMMARY:'):
                summary = line.replace('SUMMARY:', '').strip()
        
        return {
            'analysis': analysis or result_text,
            'priority': priority,
            'summary': summary or (result_text[:200] if result_text else "Pending analysis")
        }
    
    except Exception as e:
        print(f"AI Analysis Error: {e}")
        return {
            'analysis': f'AI analysis encountered an error. Manual review recommended.',
            'priority': 'Medium',
            'summary': 'Pending doctor review'
        }

@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'patient':
            return redirect(url_for('patient_portal'))
        elif session.get('role') == 'doctor':
            return redirect(url_for('doctor_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    
    if not username or not password or not role:
        flash('All fields are required.', 'error')
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND role = ?',
                       (username, role)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['full_name'] = user['full_name']
        
        if role == 'patient':
            return redirect(url_for('patient_portal'))
        else:
            return redirect(url_for('doctor_dashboard'))
    else:
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/patient/portal')
def patient_portal():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    patient_records = conn.execute(
        'SELECT * FROM patient_data WHERE patient_id = ? ORDER BY submitted_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    
    return render_template('patient_portal.html', records=patient_records)

@app.route('/patient/submit', methods=['POST'])
def submit_patient_data():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('index'))
    
    age = request.form.get('age')
    gender = request.form.get('gender')
    symptoms = request.form.get('symptoms')
    medical_history = request.form.get('medical_history')
    current_medications = request.form.get('current_medications')
    
    file_path = None
    file_name = None
    
    if 'medical_file' in request.files:
        file = request.files['medical_file']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{session['user_id']}_{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_name = file.filename
    
    patient_data = {
        'age': age,
        'gender': gender,
        'symptoms': symptoms,
        'medical_history': medical_history,
        'current_medications': current_medications
    }
    
    ai_result = analyze_patient_data_with_ai(patient_data)
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO patient_data (patient_id, age, gender, symptoms, medical_history, 
                                  current_medications, file_path, file_name, 
                                  ai_analysis, health_priority, ai_summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], age, gender, symptoms, medical_history, 
          current_medications, file_path, file_name,
          ai_result['analysis'], ai_result['priority'], ai_result['summary']))
    conn.commit()
    conn.close()
    
    flash('Your health report has been submitted successfully!', 'success')
    return redirect(url_for('patient_portal'))

@app.route('/doctor/dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    patients_data = conn.execute('''
        SELECT pd.*, u.full_name as patient_name, u.email as patient_email
        FROM patient_data pd
        JOIN users u ON pd.patient_id = u.id
        ORDER BY pd.submitted_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('doctor_dashboard.html', patients_data=patients_data)

@app.route('/doctor/add_note', methods=['POST'])
def add_doctor_note():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    patient_data_id = request.form.get('patient_data_id')
    notes = request.form.get('notes')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO doctor_notes (patient_data_id, doctor_id, notes)
        VALUES (?, ?, ?)
    ''', (patient_data_id, session['user_id'], notes))
    conn.commit()
    conn.close()
    
    flash('Your note has been added successfully!', 'success')
    return redirect(url_for('doctor_dashboard'))

@app.route('/doctor/get_notes/<int:patient_data_id>')
def get_doctor_notes(patient_data_id):
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    notes = conn.execute('''
        SELECT dn.*, u.full_name as doctor_name
        FROM doctor_notes dn
        JOIN users u ON dn.doctor_id = u.id
        WHERE dn.patient_data_id = ?
        ORDER BY dn.created_at DESC
    ''', (patient_data_id,)).fetchall()
    conn.close()
    
    return jsonify({
        'success': True,
        'notes': [dict(note) for note in notes]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
