from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    company = db.Column(db.String(100))
    speaking_points = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    proficiency_level = db.Column(db.String(20))
    instructor = db.Column(db.String(50))