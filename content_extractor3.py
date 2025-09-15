from youtube_transcript_api import YouTubeTranscriptApi
import PyPDF2 
import logging
import re

# OCR dependencies
import pytesseract
from PIL import Image
import io
from pdf2image import convert_from_bytes

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_youtube_transcript(url: str):
    match = re.search(r"(?:v=|youtu\.be/)([^&?]+)", url)
    if not match:
        return None, "Invalid YouTube URL"
    video_id = match.group(1)

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id) 
        transcript = " ".join([entry.text for entry in transcript_list])  
        return transcript, None
    except Exception as e:
        return None, str(e)
    

def get_pdf_text(pdf_file):
    """
    Extracts text from an uploaded PDF file.
    Returns the text or an error message.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        # Iterate through all pages and extract text
        for page in pdf_reader.pages:
            text += page.extract_text() or "" # Handles empty pages gracefully
        
        logging.info(f"Successfully extracted PDF text of length {len(text)}.")
        return text, None
    except Exception as e:
        error_message = f"Error extracting PDF text: {e}"
        logging.error(error_message)
        return None, error_message

def get_pdf_text_ocr(pdf_file):
    """
    Extracts text from scanned PDF using OCR (pytesseract).
    Returns the text or an error message.
    """

    try:
        # Convert PDF pages to images
        pdf_bytes = pdf_file.read()
        import os
        poppler_path = None
        if os.name == 'nt':  # Windows
            custom_path = r'C:\Users\Hemant\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin'
            if os.path.exists(custom_path):
                poppler_path = custom_path
            # Set tesseract path for Windows
            tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if os.path.exists(tess_path):
                pytesseract.pytesseract.tesseract_cmd = tess_path
        images = convert_from_bytes(pdf_bytes, poppler_path=poppler_path) if poppler_path else convert_from_bytes(pdf_bytes)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
        logging.info(f"Successfully extracted OCR text of length {len(ocr_text)}.")
        return ocr_text, None
    except Exception as e:
        error_message = f"Error extracting OCR text from PDF: {e}"
        logging.error(error_message)
        return None, error_message


