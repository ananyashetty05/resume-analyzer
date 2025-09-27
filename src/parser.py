import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_txt(txt_file):
    """Extract text from uploaded text file"""
    try:
        return txt_file.read().decode('utf-8')
    except Exception as e:
        return f"Error reading text file: {str(e)}"