# Resume Analyzer AI 🚀

A complete Resume Analyzer project utilizing Flask backend and Sentence Transformers (NLP model) to score resumes against job descriptions.

## Overview

This application allows a user to upload a resume (PDF/DOCX) and compare it against a specific job description. The AI will extract skills, find missing skills, provide a similarity match score, and generate tailored recommendations.

## Project Structure

```text
Resume-Analyzer-App/
│── app.py                 # Main Flask server
│── requirements.txt       # Python dependencies
│── templates/
│   └── index.html         # Frontend HTML structure
│── static/
│   ├── style.css          # UI styles
│   └── script.js          # API Logic and interactive UI components
│── uploads/               # Temporary storage for uploaded resumes
└── README.md              # Instructions
```

## How to Run the Project Locally

### 1. Prerequisites

- **Python 3.8+** must be installed.
- Ensure you have **pip** installed.

### 2. Setup a Virtual Environment (Recommended but optional)

Open your terminal and run:

```bash
python -m venv venv

# For Windows
venv\Scripts\activate

# For Mac/Linux
source venv/bin/activate
```

### 3. Install Requirements

Install all necessary Python dependencies by running:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the Flask server:

```bash
python app.py
```

### 5. Open Web Application

Open your browser and navigate to:

```text
http://127.0.0.1:5000/
```

Upload your resume, paste a Job Description, and start analyzing! 🎉
