import random
from bs4 import BeautifulSoup
import requests
import urllib.request

def get_text(url: str) -> str:
    """
    Retrieves and cleans up the text from a webpage specified by the given URL.

    This function accesses a webpage using the provided URL, then extracts all text from the page. 
    It uses BeautifulSoup for parsing the HTML content and removes any excessive whitespace, 
    including new lines and tabs, resulting in a cleaned, continuous block of text.

    Parameters:
    url (str): The URL of the webpage from which to extract text.

    Returns:
    str: A string containing the cleaned text extracted from the webpage. 
         If the webpage has no text content or an error occurs, an empty string is returned.
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

    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    try:
      response = requests.get(url, headers=headers, timeout=30)
      if response.status_code == 200:
        response = response.text
      else:
        print('error code != 200')                   
        raise ValueError(f'Unable to get data from pdf link: {url}')
    except:
      try:
        response = urllib.request.urlopen(url, timeout= 30)
        response = response.read().decode('utf-8')
      except Exception as e:
        raise ValueError(e)

    soup = BeautifulSoup(response, 'html.parser')
    if soup.find('main'):
      soup=soup.find('main')

    text = soup.get_text()
    cleaned_text = ' '.join(text.split())
    return cleaned_text