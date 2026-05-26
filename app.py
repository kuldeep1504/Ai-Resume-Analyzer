import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
# Configurations
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize model
print("Loading NLP model (SentenceTransformers)...")
model = SentenceTransformer('all-MiniLM-L6-v2') # lightweight bert model
print("Model loaded successfully.")

def extract_text_from_pdf(filepath):
    text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

# Extended list of common skills for extraction
COMMON_SKILLS = [
    "python", "java", "c++", "javascript", "react", "node.js", "html", "css",
    "flask", "django", "machine learning", "deep learning", "nlp", "sql", "nosql",
    "mongodb", "aws", "docker", "kubernetes", "git", "agile", "linux", "c#",
    "ruby", "php", "rest api", "graphql", "tensorflow", "pytorch", "pandas", "numpy",
    "scikit-learn", "data analysis", "devops", "ci/cd", "azure", "gcp", "fastapi"
]

def extract_skills(text):
    text_lower = text.lower()
    extracted = set()
    for skill in COMMON_SKILLS:
        if skill in text_lower:
            extracted.add(skill.title())
    return list(extracted)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400
    
    file = request.files['resume']
    job_description = request.form.get('job_description', '').strip()

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if not job_description:
        return jsonify({"error": "Job description is missing"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text based on file type
        resume_text = ""
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext == 'pdf':
            resume_text = extract_text_from_pdf(filepath)
        elif ext in ['doc', 'docx']:
            resume_text = extract_text_from_docx(filepath)
        else:
            os.remove(filepath)
            return jsonify({"error": "Unsupported file format. Please upload PDF or DOCX."}), 400

        # Remove the file after processing
        os.remove(filepath)

        if not resume_text.strip():
            return jsonify({"error": "Could not extract text from the resume."}), 400

        # 1. Skill Extraction
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(job_description)
        
        # 2. Find Missing Skills
        missing_skills = list(set(jd_skills) - set(resume_skills))

        # 3. Calculate Similarity Score
        # Encode both texts to get embeddings
        embeddings1 = model.encode(resume_text, convert_to_tensor=True)
        embeddings2 = model.encode(job_description, convert_to_tensor=True)

        # Compute cosine similarities
        cosine_score = util.cos_sim(embeddings1, embeddings2).item()
        match_percentage = round(cosine_score * 100, 2)
        match_percentage = max(0, min(100, match_percentage)) # Clamp between 0 and 100

        # Generate suggestions
        suggestions = []
        if match_percentage < 40:
            suggestions.append("Your resume needs significant tailoring to match the job description.")
        elif match_percentage < 70:
            suggestions.append("Good start, but consider adding more relevant keywords and context.")
        else:
            suggestions.append("Excellent match! Ensure your experiences clearly highlight the required skills in detail.")

        if missing_skills:
            suggestions.append(f"Consider learning or adding these missing skills to your resume: {', '.join(missing_skills[:5])}")

        return jsonify({
            "extracted_skills": resume_skills,
            "missing_skills": missing_skills,
            "match_score": match_percentage,
            "suggestions": suggestions
        })

if __name__ == '__main__':
    # Ensure uploads folder exists before running
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print("Starting Flask web server...")
    app.run(debug=True, port=5000)
