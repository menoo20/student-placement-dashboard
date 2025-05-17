import os
import sqlite3
import csv
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
app.config['DATABASE'] = 'students.db'

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
        email TEXT NOT NULL,
        national_id TEXT NOT NULL,
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
                    elif 'email' in h or 'address' in h:
                        header_mapping[h] = 'email'
                    elif 'national' in h or 'id' in h:
                        header_mapping[h] = 'national_id'
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
                    email = row_data.get('email', '')
                    national_id = row_data.get('national_id', '')
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
                    INSERT INTO students (name, email, national_id, company, speaking_points, total_points, proficiency_level, instructor)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (name, email, national_id, company, speaking_points, total_points, proficiency_level, instructor))
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
                        elif 'email' in h or 'address' in h:
                            header_mapping[h] = 'email'
                        elif 'national' in h or 'id' in h:
                            header_mapping[h] = 'national_id'
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
                        email = row_data.get('email', '')
                        national_id = row_data.get('national_id', '')
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
                        INSERT INTO students (name, email, national_id, company, speaking_points, total_points, proficiency_level, instructor)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (name, email, national_id, company, speaking_points, total_points, proficiency_level, instructor))
            except Exception as e:
                print(f"Error importing CSV with latin1 encoding: {e}")
    
    conn.commit()
    conn.close()

def get_stats():
    conn = get_db_connection()
    
    # Get total students
    cursor = conn.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]
    
    # Get proficiency level counts
    cursor = conn.execute('SELECT proficiency_level, COUNT(*) FROM students GROUP BY proficiency_level')
    proficiency_counts = {}
    for row in cursor.fetchall():
        proficiency_counts[row[0]] = row[1]
    
    # Get instructor counts
    cursor = conn.execute('SELECT instructor, COUNT(*) FROM students GROUP BY instructor')
    instructor_counts = {}
    for row in cursor.fetchall():
        instructor_counts[row[0]] = row[1]
    
    # Get average score
    cursor = conn.execute('SELECT AVG(total_points) FROM students')
    avg_score = cursor.fetchone()[0] or 0
    
    # Get score distribution
    score_ranges = {
        '0-9': 0,
        '10-19': 0,
        '20-29': 0,
        '30-39': 0,
        '40-49': 0,
        '50-59': 0,
        '60+': 0
    }
    
    cursor = conn.execute('SELECT total_points FROM students')
    for row in cursor.fetchall():
        score = row[0]
        if score < 10:
            score_ranges['0-9'] += 1
        elif score < 20:
            score_ranges['10-19'] += 1
        elif score < 30:
            score_ranges['20-29'] += 1
        elif score < 40:
            score_ranges['30-39'] += 1
        elif score < 50:
            score_ranges['40-49'] += 1
        elif score < 60:
            score_ranges['50-59'] += 1
        else:
            score_ranges['60+'] += 1
    
    conn.close()
    
    return {
        'total_students': total_students,
        'proficiency_counts': proficiency_counts,
        'instructor_counts': instructor_counts,
        'avg_score': avg_score,
        'score_ranges': score_ranges
    }

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    
    stats = get_stats()
    
    return render_template('index.html', students=students, stats=stats)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    national_id = request.form['national_id']
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
    INSERT INTO students (name, email, national_id, company, speaking_points, total_points, proficiency_level, instructor)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, national_id, company, speaking_points, total_points, proficiency_level, instructor))
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
        'email': student['email'],
        'national_id': student['national_id'],
        'company': student['company'],
        'speaking_points': student['speaking_points'],
        'total_points': student['total_points'],
        'proficiency_level': student['proficiency_level'],
        'instructor': student['instructor']
    })

@app.route('/update_student/<int:id>', methods=['POST'])
def update_student(id):
    name = request.form['name']
    email = request.form['email']
    national_id = request.form['national_id']
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
    UPDATE students
    SET name = ?, email = ?, national_id = ?, company = ?, speaking_points = ?, 
        total_points = ?, proficiency_level = ?, instructor = ?
    WHERE id = ?
    ''', (name, email, national_id, company, speaking_points, total_points, 
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
    
    return redirect(url_for('index'))

@app.route('/reset_database', methods=['GET'])
def reset_database():
    conn = get_db_connection()
    conn.execute('DROP TABLE IF EXISTS students')
    conn.close()
    
    # Reinitialize the database
    init_db()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the app
    app.run(host='0.0.0.0', port=5001, debug=True)
