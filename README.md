
# 📄 AI-Powered Resume Analyzer

## 📝 Problem Statement
Recruiters often spend only a few seconds scanning resumes. Many candidates struggle to optimize their resumes for Applicant Tracking Systems (ATS) and specific job descriptions.  
This project analyzes resumes using **NLP + AI** to provide:  
- A similarity score between resume and job description  
- Missing keywords  
- Actionable suggestions for improvement  
## 📝 Overview
AI-Powered Resume Analyzer is a tool that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and specific job descriptions. Using Natural Language Processing (NLP) and AI, it analyzes resumes and provides actionable insights to improve their effectiveness.
Recruiters often spend only a few seconds scanning resumes. Many candidates struggle to optimize their resumes for Applicant Tracking Systems (ATS) and specific job descriptions. This project analyzes resumes using **NLP + AI** to provide actionable insights and improvements.


## 🎯 Key Features
- Resume analysis against job descriptions using NLP
- ATS compatibility scoring and feedback
- Keyword gap analysis and suggestions
- Smart recommendations for resume improvement
- Support for PDF and TXT resume formats
- User-friendly web interface built with Streamlit

## 🚀 Features
- ✅ Upload Resume in **PDF or TXT** format  
- ✅ Paste a **Job Description (JD)**  
- ✅ Extract key information using **NLP (spaCy + NLTK)**  
- ✅ Compute similarity using **Sentence-BERT embeddings**  
- ✅ Generate a **Resume Score (%)**  
- ✅ Provide **ATS-friendly suggestions**  
- ✅ Simple **Streamlit web app** interface  

## 🛠️ Technologies Used
- Python 3.8+
- spaCy & NLTK for NLP
- Sentence-BERT for semantic similarity
- spaCy & NLTK for Natural Language Processing
- Sentence-BERT for semantic similarity scoring
- Streamlit for web application interface
- PyPDF2 for PDF document processing

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Steps to Install

1. Clone the repositorybash
git clone https://github.com/ananyashetty05/resume-analyzer.git
cd resume-analyzer
2. Create
- Streamlit for web interface
- PyPDF2 for PDF processing

---
## 📦 Installation

## 📂 Project Structure
resume-analyzer/
│── data/ # Sample resumes & job descriptions
│── src/
1. Clone the repositorybash
git clone https://github.com/ananyashetty05/resume-analyzer.git
cd resume-analyzer
2. Create an
│ ├── parser.py # Extract text from resumes
│ ├── nlp_utils.py # NLP preprocessing & keyword extraction
│ ├── scorer.py # Resume vs JD scoring logic
│ ├── app.py # Streamlit app
│── requirements.txt # Dependencies
│── README.md # Project documentation
│── venv/ # Virtual environment (ignored in Git)

