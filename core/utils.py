import re
import fitz  # PyMuPDF
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "Unsupported file format. Please upload a PDF or text file."

# Need to rework this function
def calculate_match_score(resume_text, job_description):
    def preprocess(text):
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text
    
    resume_processed = preprocess(resume_text)
    job_processed = preprocess(job_description)

    vectorizer = CountVectorizer(stop_words='english', ngram_range=(1, 2))
    job_matrix = vectorizer.fit_transform([job_processed])
    job_words = vectorizer.get_feature_names_out()

    resume_matrix = vectorizer.transform([resume_processed])
    job_word_count = job_matrix.sum()
    matched_words = (resume_matrix > 0).multiply(job_matrix).sum()

    if job_word_count > 0:
        match_percentage = (matched_words / job_word_count) * 100
    else:
        match_percentage = 0

    job_count = Counter({word: job_matrix[0, i] for i, word in enumerate(job_words)})
    resume_count = Counter({word: resume_matrix[0, i] for i, word in enumerate(job_words)})

    missing_words = [word for word, count in job_count.items() 
                     if word not in resume_count or resume_count[word] < count]

    missing_words.sort(key=lambda x: job_count[x], reverse=True)
    top_missing = missing_words[:20]

    return {
        'match_percentage': round(match_percentage, 2),
        'missing_keywords': top_missing
    }
