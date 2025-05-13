from flask import Flask, render_template, request, send_file, session
#.\jobfit_env\Scripts\activate
import os
import sqlite3
from werkzeug.utils import secure_filename
from docx import Document
from io import BytesIO
from pdfminer.high_level import extract_text
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# List of known skills
skill_keywords = [
    "python", "java", "sql", "html", "css", "javascript",
    "machine learning", "data analysis", "django", "flask"
]

# ---------- Helper Functions ----------
def extract_pdf_text(file_path):
    return extract_text(file_path)

def extract_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_skills_basic(text):
    text_lower = text.lower()
    return [skill for skill in skill_keywords if skill in text_lower]

def match_jobs(user_skills):
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, skills FROM job_roles")
    job_matches = []
    for title, skills in cursor.fetchall():
        job_skills = [s.strip().lower() for s in skills.split(',')]
        score = len(set(user_skills) & set(job_skills)) / len(set(job_skills))
        missing = list(set(job_skills) - set(user_skills))
        job_matches.append((title, score, missing))
    conn.close()
    job_matches.sort(key=lambda x: x[1], reverse=True)
    return job_matches  # Removed [:5] to show all jobs

from textwrap import wrap

def generate_pdf_report(user_skills, matches):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    left_margin = 50
    right_margin = 50
    usable_width = width - left_margin - right_margin
    y = height - 50  # Top margin
    line_height = 20

    def draw_wrapped_text(text, font_size=12):
        nonlocal y
        c.setFont("Helvetica", font_size)
        wrapped_lines = wrap(text, width=100)  # adjust based on font size
        for line in wrapped_lines:
            if y <= 50:
                c.showPage()
                y = height - 50
            c.drawString(left_margin, y, line)
            y -= line_height

    def draw_header():
        nonlocal y
        c.setFont("Helvetica-Bold", 14)
        c.drawString(left_margin, y, "JobFit AI Report")
        y -= line_height
        draw_wrapped_text(f"Skills Detected: {', '.join(user_skills)}")
        y -= line_height

    draw_header()

    for role, score, missing in matches:
        if y <= 80:
            c.showPage()
            y = height - 50
            draw_header()

        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_margin, y, f"Role: {role} | Match: {score * 100:.2f}%")
        y -= line_height
        c.setFont("Helvetica", 12)
        missing_str = ', '.join(missing) if missing else 'None'
        draw_wrapped_text(f"Missing Skills: {missing_str}")
        y -= 10  # extra space between roles

    c.save()
    buffer.seek(0)
    return buffer



# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return 'No file uploaded', 400
    file = request.files['resume']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    if filename.endswith('.pdf'):
        text = extract_pdf_text(path)
    elif filename.endswith('.docx'):
        text = extract_docx_text(path)
    else:
        return 'Unsupported file type', 400

    user_skills = extract_skills_basic(text)
    matches = match_jobs(user_skills)

    # Store in session for download
    session['skills'] = user_skills
    session['matches'] = matches

    return render_template('report.html', skills=user_skills, matches=matches)

@app.route('/download')
def download_report():
    skills = session.get('skills', [])
    matches = session.get('matches', [])
    report = generate_pdf_report(skills, matches)
    return send_file(report, as_attachment=True, download_name='JobFit_Report.pdf')

# ---------- Start App ----------
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
