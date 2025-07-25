
from flask import Flask, render_template, request, redirect, send_file
import csv
import os

app = Flask(__name__)
CSV_FILE = os.environ.get('CSV_FILE_PATH', 'students.csv')

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Roll No', 'Name', 'Email', 'Gender', 'Contact', 'DOB', 'Address'])

def read_students():
    with open(CSV_FILE, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_students(students):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=students[0].keys())
        writer.writeheader()
        writer.writerows(students)

@app.route('/')
def index():
    students = read_students()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    new_student = {
        'Roll No': request.form['roll'],
        'Name': request.form['name'],
        'Email': request.form['email'],
        'Gender': request.form['gender'],
        'Contact': request.form['contact'],
        'DOB': request.form['dob'],
        'Address': request.form['address']
    }
    students = read_students()
    students.append(new_student)
    write_students(students)
    return redirect('/')

@app.route('/delete/<roll>')
def delete_student(roll):
    students = read_students()
    students = [s for s in students if s['Roll No'] != roll]
    write_students(students)
    return redirect('/')

@app.route('/download')
def download_csv():
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
