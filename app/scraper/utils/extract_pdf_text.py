import requests
import fitz
from .split_text import split_text
import time
import re
import urllib.request
import random

def extract_pdf_text(URL:str):
    """
    Extracts and returns all text from a PDF document located at the specified URL.

    This function downloads a PDF file from the provided URL using an HTTP GET request. It then opens the PDF
    using PyMuPDF (fitz) to iterate through each page of the document, extracting all text content. The text
    from each page is cleaned by splitting and rejoining to ensure there is no excessive whitespace. The function
    currently does not extract text from images within the PDF but includes commented-out code as a placeholder
    for future functionality using pytesseract for OCR.

    Parameters:
    - URL (str): The URL of the PDF document from which text is to be extracted.

    Returns:
    - str: A string containing all extracted text from the PDF, with text from different pages separated by newlines.

    Note:
    - The function uses `requests` for downloading the PDF and `PyMuPDF` (fitz) for reading the PDF content.
    - Ensure that both `requests` and `PyMuPDF` (fitz) libraries, along with any dependencies for image extraction
      and OCR (like `Pillow` for image handling and `pytesseract` for OCR), are installed and properly configured
      in your environment before using the function.
    - The commented-out section for extracting text from images within the PDF suggests a potential enhancement
      for the function, requiring additional libraries such as `io`, `Pillow` (PIL), and `pytesseract`.
    """
    
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 10; en-us; SM-G960U Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    ]

    extracted_text=[]
    retries=0
    while retries<=5:
        try:
            pdf_response = requests.get(URL, timeout=20, headers = {'User-Agent':random.choice(user_agents)})
            if pdf_response.status_code==200:
                pdf_response = pdf_response.content
                break
            else:                 
                if retries==5:
                    raise ValueError(f'Unable to get data from pdf link: {URL}')
                retries+=1
                time.sleep(5)
                continue
        except Exception as e:
            try:
                pdf_response = urllib.request.urlopen(URL, timeout= 20)
                pdf_response = pdf_response.read()
                break
            except Exception as e:
                if retries==5:
                    raise ValueError(e)
                retries+=1
                time.sleep(5)
                continue
            
    pdf_scraper = fitz.open(stream=pdf_response)

    # iterate the document pages

    for page in pdf_scraper: 
        # Extract text from pdf document
        text = page.get_text() # get plain text encoded as UTF-8
        text = re.sub(r'\n\s*\n', '\n\n', text)
        extracted_text.append(text)
        split=split_text(9000,0,'\n'.join(extracted_text))
        if len(split)>1:
            break
    all_text="\n".join(extracted_text)
    return all_text