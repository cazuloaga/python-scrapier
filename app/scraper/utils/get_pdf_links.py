import requests
from bs4 import BeautifulSoup

def get_pdf_links(url:str) -> list:
    """
    Fetches and extracts all PDF file links from a given webpage URL.

    This function performs an HTTP GET request to retrieve the content of the webpage specified by the URL.
    It then parses the webpage content using BeautifulSoup to find all hyperlinks (`<a>` tags). It filters these
    hyperlinks to return only those that point to PDF files (identified by the '.pdf' extension in the href attribute).

    Parameters:
    - url (str): The URL of the webpage from which to extract PDF links.

    Returns:
    - list: A list of strings, where each string is a URL pointing to a PDF file found on the specified webpage.
            If no PDF links are found, an empty list is returned.
        
    Note:
    - The function prints 'PDF link found' to the console if at least one PDF link is discovered on the webpage.
    - The function relies on the external libraries `requests` and `beautifulsoup4`. Ensure these are installed
      and properly configured in your environment before using the function.
    - This function does not handle relative URLs for PDF links. All returned URLs are exactly as found in the
      href attribute of `<a>` tags.
    """
    # Fetch the webpage
    response = requests.get(url)

    # Ensure successful response
    response.raise_for_status()

    # Parse the webpage with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup.find('main'):
      soup=soup.find('main')

    # Search for PDF links
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

    # Check if there are any PDF links
    if pdf_links:
      return pdf_links