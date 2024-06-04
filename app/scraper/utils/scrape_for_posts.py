import random
from urllib import request
from urllib.error import URLError
import requests
from bs4 import BeautifulSoup
from .logger import logger
from app import schemas

def scrape_for_posts(website: schemas.Website):
    """
    Parses a webpage to find specific HTML elements based on provided criteria.

    This function loads the webpage at the given URL and uses BeautifulSoup to parse it. 
    It first searches for an 'outer' HTML element as specified by `outer_html`, and within that element, 
    it searches for an 'inner' HTML element as specified by `inner_html`.

    Parameters:
    url (str): The URL of the webpage to be parsed.
    inner_html (dict): A dictionary containing the tag and class of the inner HTML element to be found. 
                       The dictionary should have keys 'tag' and 'class'.
    outer_html (dict): A dictionary containing the tag and class of the outer HTML element to be found. 
                       The dictionary should have keys 'tag' and 'class'.

    Returns:
    BeautifulSoup object: The found inner HTML element, or None if the element is not found.

    Raises:
    urllib.error.URLError: If the URL is invalid or unreachable.
    Exception: If there's an error in parsing the HTML content.
    """
    url=website.website
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
        response = requests.get(url, headers=headers, timeout=60)
        response = response.text
    except requests.exceptions.Timeout:
        # Attempt using urllib
        try:
            response = request.urlopen(url, timeout=60).read().decode('utf-8')
        except URLError as e:
            raise URLError(f"Error accessing URL: {e}")
    except Exception as e:
        logger.warning(f'Unable to extract alerts from {url}. Error: {e}')
        return []

    soup = BeautifulSoup(response, 'html.parser')
    alerts = []
    
    # Find the outer element first
    if website.outer_type_value != None:
        outer = soup.find_all(website.outer_tag, class_=website.outer_type_value)
        if not outer:
            return []
        # Find the inner element second
        if website.inner_type_value != None:
            for item in outer:
                alerts += item.find_all(website.inner_tag, class_=website.inner_type_value)

        else:
            for item in outer:
                alerts += item.find_all(website.inner_tag)
    else:
        outer = soup.find_all(website.outer_tag)
        if not outer:
            return []
        if website.inner_type_value != None:
            for item in outer:
                alerts += item.find_all(website.inner_tag, class_=website.inner_type_value)
        else:
            for item in outer:
                alerts += item.find_all(website.inner_tag)

    return alerts