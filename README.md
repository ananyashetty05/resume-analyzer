# 📄 AI-Powered Resume Analyzer

## 📝 Overview
AI-Powered Resume Analyzer is an advanced tool that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and specific job descriptions. Using Natural Language Processing (NLP) and optional AI integration, it provides comprehensive analysis and actionable insights.

## 🎯 Key Features
- **Comprehensive Skills Analysis** - Detailed matching of your skills vs job requirements
- **AI-Powered Insights** - Optional OpenAI integration for advanced analysis
- **Keyword Gap Analysis** - Identifies missing keywords and phrases
- **ATS Compatibility Scoring** - Ensures your resume passes automated screening
- **Section Structure Analysis** - Checks for proper resume organization
- **Actionable Recommendations** - Specific suggestions for improvement
- **Multi-format Support** - PDF and TXT resume uploads
- **Interactive Dashboard** - User-friendly Streamlit interface

## 🚀 Enhanced Features
- ✅ **Skills Matching** - Shows exactly which skills match and which are missing
- ✅ **Critical vs Nice-to-Have** - Prioritizes skill gaps by importance
- ✅ **AI Analysis** - Advanced insights when OpenAI API key is provided
- ✅ **Content Recommendations** - Specific content to add/remove
- ✅ **Action Verb Suggestions** - Stronger language recommendations
- ✅ **Quantifiable Achievements** - Guidance on adding metrics
- ✅ **Experience Matching** - How well your experience aligns with the role

## 🛠️ Technologies Used
- **Python 3.8+** - Core programming language
- **Streamlit** - Web application framework
- **spaCy & NLTK** - Natural Language Processing
- **Scikit-learn** - Machine learning for similarity analysis
- **OpenAI API** - Optional AI-powered analysis
- **PyPDF2** - PDF document processing

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/ananyashetty05/resume-analyzer.git
cd resume-analyzer
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Optional: Setup AI Analysis**
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your-api-key-here
```

5. **Launch the application**
```bash
cd src
streamlit run app.py
```

## 🎯 How to Use

1. **Upload Resume** - Support for PDF and TXT formats
2. **Paste Job Description** - Copy the complete job posting
3. **Click Analyze** - Get comprehensive feedback in seconds
4. **Review Results** - Check scores, gaps, and recommendations
5. **Take Action** - Implement suggested improvements

## 📊 Analysis Features

### Skills Analysis
- **Matching Skills** - Skills you have that match the job
- **Missing Critical Skills** - Essential skills you need to add
- **Nice-to-Have Skills** - Bonus skills for competitive advantage
- **Skill Match Percentage** - Overall skills alignment score

### Keyword Analysis
- **Job Keywords** - Important terms from the job description
- **Missing Keywords** - Terms to incorporate in your resume
- **Keyword Coverage** - How well your resume covers key terms

### AI Insights (Optional)
- **Strengths & Weaknesses** - AI-detected resume qualities
- **Specific Improvements** - Targeted enhancement suggestions
- **ATS Recommendations** - Formatting and structure advice
- **Action Verbs** - Stronger language alternatives

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### Without AI
The application works fully without OpenAI integration, providing:
- NLP-based analysis
- Skills matching
- Keyword analysis
- ATS scoring
- Structure recommendations

## 📂 Project Structure
```
resume-analyzer/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── parser.py           # PDF/TXT text extraction
│   ├── nlp_utils.py        # NLP processing utilities
│   ├── scorer.py           # Resume scoring logic
│   └── ai_analyzer.py      # AI-powered analysis
├── data/                   # Sample files (optional)
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🚀 Features in Detail

### Traditional Analysis
- **TF-IDF Similarity** - Content matching using machine learning
- **Skills Extraction** - Comprehensive skill detection
- **Section Analysis** - Resume structure evaluation
- **Weak Word Detection** - Language improvement suggestions

### AI-Enhanced Analysis
- **Contextual Understanding** - Deeper content analysis
- **Industry-Specific Insights** - Role-relevant recommendations
- **Personalized Feedback** - Tailored improvement suggestions
- **Advanced Pattern Recognition** - Subtle optimization opportunities

## 💡 Pro Tips
- Use keywords from the job description naturally throughout your resume
- Quantify achievements with specific numbers and percentages
- Tailor your resume for each job application
- Focus on critical missing skills first
- Use strong action verbs to describe accomplishments
- Ensure proper ATS formatting for automated screening

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.

## 🙏 Acknowledgments
- Built with Streamlit for the web interface
- Powered by spaCy and NLTK for NLP processing
- Enhanced with OpenAI for advanced AI analysis
- Inspired by the need for better resume optimization tools

---
**Built with ❤️ using Python, NLP & AI**