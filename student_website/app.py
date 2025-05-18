import os
import sqlite3
import csv
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
app.config['DATABASE'] = 'students.db'

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "menoo20"  # fallback to your known password

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def normalize_header(header):
    # Remove leading/trailing spaces, colons, and convert to lowercase
    return header.strip().rstrip(':').lower()

def init_db():
    conn = get_db_connection()
    
    # Create table if it doesn't exist
    conn.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company TEXT,
        speaking_points INTEGER,
        total_points INTEGER NOT NULL,
        proficiency_level TEXT NOT NULL,
        instructor TEXT NOT NULL
    )
    ''')
    
    # Check if table is empty
    cursor = conn.execute('SELECT COUNT(*) FROM students')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Import data from CSV using standard Python libraries
        try:
            with open('data/Placement_Test_BG1_Organized.csv', 'r', encoding='utf-8-sig') as file:
                # Read the first line to get headers
                header_line = file.readline().strip()
                headers = [normalize_header(h) for h in header_line.split(',')]
                
                # Create a mapping from normalized headers to expected column names
                header_mapping = {}
                for h in headers:
                    if 'name' in h:
                        header_mapping[h] = 'name'
                    elif 'company' in h:
                        header_mapping[h] = 'company'
                    elif 'speaking' in h:
                        header_mapping[h] = 'speaking_points'
                    elif 'total' in h:
                        header_mapping[h] = 'total_points'
                    elif 'proficiency' in h:
                        header_mapping[h] = 'proficiency_level'
                    elif 'instructor' in h:
                        header_mapping[h] = 'instructor'
                
                # Reset file pointer to beginning
                file.seek(0)
                
                # Skip header line
                next(file)
                
                # Process each line manually
                for line in file:
                    # Handle potential commas within quoted fields
                    fields = []
                    in_quotes = False
                    current_field = ""
                    
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:
                            fields.append(current_field)
                            current_field = ""
                        else:
                            current_field += char
                    
                    # Add the last field
                    fields.append(current_field)
                    
                    # Map fields to their correct positions
                    row_data = {}
                    for i, field in enumerate(fields):
                        if i < len(headers):
                            normalized_header = headers[i]
                            if normalized_header in header_mapping:
                                mapped_header = header_mapping[normalized_header]
                                row_data[mapped_header] = field.strip()
                    
                    # Extract data with fallbacks
                    name = row_data.get('name', '')
                    company = row_data.get('company', '')
                    
                    # Handle potential missing or non-numeric values
                    try:
                        speaking_points = int(row_data.get('speaking_points', '0').strip())
                    except (ValueError, TypeError):
                        speaking_points = 0
                        
                    try:
                        total_points = int(row_data.get('total_points', '0').strip())
                    except (ValueError, TypeError):
                        total_points = 0
                    
                    # Determine proficiency level and instructor
                    if total_points < 30:
                        proficiency_level = 'Beginner'
                        instructor = 'Mr. Tawfeek'
                    else:
                        proficiency_level = 'Intermediate'
                        instructor = 'Mr. Mohammed Ameen'
                    
                    # Insert data into the database
                    conn.execute('''
                    INSERT INTO students (name, company, speaking_points, total_points, proficiency_level, instructor)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (name, company, speaking_points, total_points, proficiency_level, instructor))
        except Exception as e:
            print(f"Error importing CSV with UTF-8: {e}")
            
            # Fallback to try with different encoding if utf-8 fails
            try:
                with open('data/Placement_Test_BG1_Organized.csv', 'r', encoding='latin1') as file:
                    # Read the first line to get headers
                    header_line = file.readline().strip()
                    headers = [normalize_header(h) for h in header_line.split(',')]
                    
                    # Create a mapping from normalized headers to expected column names
                    header_mapping = {}
                    for h in headers:
                        if 'name' in h:
                            header_mapping[h] = 'name'
                        elif 'company' in h:
                            header_mapping[h] = 'company'
                        elif 'speaking' in h:
                            header_mapping[h] = 'speaking_points'
                        elif 'total' in h:
                            header_mapping[h] = 'total_points'
                        elif 'proficiency' in h:
                            header_mapping[h] = 'proficiency_level'
                        elif 'instructor' in h:
                            header_mapping[h] = 'instructor'
                    
                    # Reset file pointer to beginning
                    file.seek(0)
                    
                    # Skip header line
                    next(file)
                    
                    # Process each line manually
                    for line in file:
                        # Handle potential commas within quoted fields
                        fields = []
                        in_quotes = False
                        current_field = ""
                        
                        for char in line:
                            if char == '"':
                                in_quotes = not in_quotes
                            elif char == ',' and not in_quotes:
                                fields.append(current_field)
                                current_field = ""
                            else:
                                current_field += char
                        
                        # Add the last field
                        fields.append(current_field)
                        
                        # Map fields to their correct positions
                        row_data = {}
                        for i, field in enumerate(fields):
                            if i < len(headers):
                                normalized_header = headers[i]
                                if normalized_header in header_mapping:
                                    mapped_header = header_mapping[normalized_header]
                                    row_data[mapped_header] = field.strip()
                        
                        # Extract data with fallbacks
                        name = row_data.get('name', '')
                        company = row_data.get('company', '')
                        
                        # Handle potential missing or non-numeric values
                        try:
                            speaking_points = int(row_data.get('speaking_points', '0').strip())
                        except (ValueError, TypeError):
                            speaking_points = 0
                            
                        try:
                            total_points = int(row_data.get('total_points', '0').strip())
                        except (ValueError, TypeError):
                            total_points = 0
                        
                        # Determine proficiency level and instructor
                        if total_points < 30:
                            proficiency_level = 'Beginner'
                            instructor = 'Mr. Tawfeek'
                        else:
                            proficiency_level = 'Intermediate'
                            instructor = 'Mr. Mohammed Ameen'
                        
                        # Insert data into the database
                        conn.execute('''
                        INSERT INTO students (name, company, speaking_points, total_points, proficiency_level, instructor)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', (name, company, speaking_points, total_points, proficiency_level, instructor))
            except Exception as e:
                print(f"Error importing CSV with latin1 encoding: {e}")
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    password = request.form.get('password', '')
    if not password or password != ADMIN_PASSWORD:
        # Support AJAX: return JSON if requested, else plain error
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Unauthorized: Incorrect password'}), 403
        return "Unauthorized: Incorrect password", 403

    name = request.form['name']
    company = request.form['company']
    speaking_points = int(request.form['speaking_points'])
    total_points = int(request.form['total_points'])
    
    # Determine proficiency level and instructor
    if total_points < 30:
        proficiency_level = 'Beginner'
        instructor = 'Mr. Tawfeek'
    else:
        proficiency_level = 'Intermediate'
        instructor = 'Mr. Mohammed Ameen'
    
    conn = get_db_connection()
    conn.execute('''
    INSERT INTO students (name, company, speaking_points, total_points, proficiency_level, instructor)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, company, speaking_points, total_points, proficiency_level, instructor))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/get_student/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify({
        'id': student['id'],
        'name': student['name'],
        'company': student['company'],
        'speaking_points': student['speaking_points'],
        'total_points': student['total_points'],
        'proficiency_level': student['proficiency_level'],
        'instructor': student['instructor']
    })

@app.route('/update_student/<int:id>', methods=['POST'])
def update_student(id):
    name = request.form['name']
    company = request.form['company']
    new_speaking_points = int(request.form['speaking_points'])
    new_total_points = int(request.form['total_points'])

    conn = get_db_connection()
    student = conn.execute('SELECT speaking_points, total_points FROM students WHERE id = ?', (id,)).fetchone()
    if student:
        old_speaking_points = student['speaking_points'] or 0
        old_total_points = student['total_points'] or 0
        # Calculate the difference in speaking points
        diff = new_speaking_points - old_speaking_points
        # Adjust total_points by the difference
        adjusted_total_points = old_total_points + diff
        # If the user also changed total_points field directly, use the higher value
        # (or you can choose to always use the adjusted value)
        total_points = adjusted_total_points
    else:
        # Fallback: use the submitted value
        total_points = new_total_points

    # Determine proficiency level and instructor
    if total_points < 30:
        proficiency_level = 'Beginner'
        instructor = 'Mr. Tawfeek'
    else:
        proficiency_level = 'Intermediate'
        instructor = 'Mr. Mohammed Ameen'

    conn.execute('''
    UPDATE students
    SET name = ?, company = ?, speaking_points = ?, 
        total_points = ?, proficiency_level = ?, instructor = ?
    WHERE id = ?
    ''', (name, company, new_speaking_points, total_points,
          proficiency_level, instructor, id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    # Support AJAX: return JSON if requested, else redirect
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
    return redirect(url_for('index'))

@app.route('/delete_students', methods=['POST'])
def delete_students():
    ids = request.json.get('ids', [])
    if not ids:
        return jsonify({'error': 'No IDs provided'}), 400
    conn = get_db_connection()
    conn.executemany('DELETE FROM students WHERE id = ?', [(i,) for i in ids])
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/reset_database', methods=['GET'])
def reset_database():
    conn = get_db_connection()
    conn.execute('DROP TABLE IF EXISTS students')
    conn.close()
    
    # Reinitialize the database
    init_db()
    
    return redirect(url_for('index'))

@app.route('/api/student_stats')
def api_student_stats():
    conn = get_db_connection()
    students = conn.execute('SELECT proficiency_level, instructor FROM students').fetchall()
    conn.close()

    # Count proficiency levels
    beginner = sum(1 for s in students if s['proficiency_level'] == 'Beginner')
    intermediate = sum(1 for s in students if s['proficiency_level'] == 'Intermediate')

    # Count instructors
    tawfeek = sum(1 for s in students if s['instructor'] == 'Mr. Tawfeek')
    mohammed = sum(1 for s in students if s['instructor'] == 'Mr. Mohammed Ameen')

    return jsonify({
        "proficiency": {
            "labels": ["Beginner", "Intermediate"],
            "counts": [beginner, intermediate]
        },
        "instructor": {
            "labels": ["Mr. Tawfeek", "Mr. Mohammed Ameen"],
            "counts": [tawfeek, mohammed]
        }
    })

if __name__ == '__main__':
    # Initialize the database (optional, for local dev)
    init_db()
    
    # Run the app
    app.run(host='0.0.0.0', port=5001, debug=True)

# For production (e.g., Render), always initialize DB at import time:
init_db()
