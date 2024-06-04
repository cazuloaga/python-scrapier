from urllib.parse import urlparse
from .get_text import get_text
from .get_pdf_links import get_pdf_links
from .is_full_link import is_full_link
from .extract_pdf_text import extract_pdf_text
from .logger import logger
import time

def get_post_text(link_to_the_alert: str):
    """
    Retrieves and aggregates text content from a specified alert webpage and any linked PDF documents.

    This function initially checks if the provided link leads directly to a PDF document. If so, it retrieves
    the text content of the PDF. If not, it fetches the main text of the alert from the given webpage URL. It
    extracts the base URL of the website to handle potential fully qualified PDF links correctly. The function
    then explores the webpage for any linked PDFs, extracting text from each PDF, whether the link is relative
    or absolute. Finally, it concatenates all gathered text into a single string, which is returned.

    Parameters:
    - link_to_the_alert (str): The URL of the alert webpage from which to extract text.

    Returns:
    - str: A string containing the aggregated text content from the webpage and any linked PDFs. If no text
           is found, or if an error occurs during the process, an empty string is returned.

    Note:
    - The function relies on other functions: `get_text` to fetch text from the webpage, `get_pdf_links` to find
      PDF links on the webpage, and `extract_pdf_text` to extract text from the PDFs. These functions must be
      defined and correctly working for `get_alert_text` to function as intended.
    - The function includes error handling to gracefully handle any failures during text retrieval from the webpage
      or linked PDFs. In case of any exception, it falls back to returning whatever text has been gathered so far,
      or an empty string if none.
    - The function assumes the existence of a helper function `is_full_link` to check if a PDF link is a full URL
      or a relative path. This is used to correctly format PDF URLs for text extraction.
    """
    pdf_links = []
    retries = 0
    while retries<=5:
      if link_to_the_alert.endswith(".pdf"):
        text = ""
        pdf_links = [link_to_the_alert] 
        break
      try:
        text = get_text(link_to_the_alert)

        # Pull out the base url of the website to create a clickable link to alert page
        url = urlparse(link_to_the_alert)
        base_url = f"{url.scheme}://{url.netloc}"
        break
      except Exception as e:
        if retries==5:
            logger.warning(f'Unable to extract text from link {link_to_the_alert}. Error: {e}')
            return ""
        retries += 1 
        time.sleep(10)
        # Optionally check if a PDF exists on the alert webpage. If so, extract PDF text
        
    try:
      if not pdf_links:
        pdf_links = get_pdf_links(link_to_the_alert)
      if pdf_links:
        text += "\n\n"
        for pdf_link in pdf_links:
            if not is_full_link(pdf_link):
                pdf_text = extract_pdf_text(base_url+pdf_link)
                text += pdf_text
                text += "\n\n"
            else:
                pdf_text = extract_pdf_text(pdf_link)
                text += pdf_text
                text += "\n\n"
      return text
    except Exception as e:
        return text
            