
from urllib.parse import urlparse
from .utils.scrape_for_posts import scrape_for_posts
from .utils.is_full_link import is_full_link
from .utils.call_gpt import call_chat_GPT
from .utils.prompts import parse_post_prompt_links, parse_post_prompt
from .utils.post_text import get_post_text
from .utils.extract_href import extract_href
from .utils.split_text import split_text
from .utils.helper_func import *
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from .utils.logger import logger
from .. import schemas
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive","https://spreadsheets.google.com/feeds"]
SERVICE_ACCOUNT_FILE = 'creds.json'

def scrape_website(website: schemas.Website, db: Session = Depends(get_db), limit = 10) -> list[schemas.PostCreateAuto] :
    """
    Processes alerts from a given webpage for a specific date, updates the database, and returns the alerts data.

    This function takes a webpage URL and a date, then uses provided file paths for website HTML information and
    data storage to scrape, process, and store alert information. It retrieves website-specific scraping parameters
    from a JSON file, scrapes the webpage for alerts, processes each alert to extract and format its information,
    checks for the existence of each alert in the database, and updates the database with new alerts. The function
    returns a list of dictionaries containing processed alerts data for the given date.

    Parameters:
    - webpage (str): The URL of the webpage to scrape for alerts.
    - date (str): The target date for which alerts are processed and returned, formatted as 'mm/dd/yyyy'.
    - web_file_path (str): The file path to the JSON file containing website-specific scraping parameters.
    - data_file_path (str): The file path to the SQLite database file where alerts data is stored.

    Returns:
    - list: A list of dictionaries, each representing an alert for the given date with keys 'publication_date',
            'link_to_the_alert', and 'text_of_the_alert'. If no new alerts are found or processed, returns an empty list.

    Note:
    - The function integrates several external functionalities including website lookup for scraping parameters,
      scraping for alerts based on HTML structure, processing alerts through a GPT model for structured data,
      checking for alert existence in the database, and updating the database with new alerts.
    - The function handles JSON parsing with error catching to gracefully manage malformed JSON responses from GPT.
    - It utilizes a helper function `is_full_link` to determine if extracted alert links are relative or absolute,
      and formats them accordingly.
    - Database connections are opened and closed within the function, ensuring resource management and data integrity.
    - The function is designed to be the primary entry point for processing and storing alerts data from a webpage,
      suitable for scheduled execution or manual invocation with specific parameters.
    """
    webpage = website.website
    url = urlparse(webpage)
    base_url = f"{url.scheme}://{url.netloc}"

    results = []

    # Find the website in our JSON file with all the website HTML information 
    print('Scraping website:', webpage)
    alerts_html = scrape_for_posts(website)
    if alerts_html==[]:
        return results
    
    for html in alerts_html[0:limit]:
        html_str=str(html)            
        # Check if there is a unique href inside <a> tag
        links=extract_href(html)
        if len(links)==1:
            link=links[0]
            logger.info(f'Link from html - {link}')

        else:
            valid_link = False
            for new_link in links:
                if new_link.startswith('https:') or new_link.startswith('http:'):
                    link = new_link
                    valid_link = True
                    break
            
            if not valid_link:
                # Call GPT to extract link
                prompt = parse_post_prompt_links(html_str, links)
                link = call_chat_GPT(prompt)
                link = link.content
                if links:
                    if link not in links:
                        logger.warning(f'Link from gpt not valid - {link}')
                        continue
                    else:
                        logger.info(f'Link from gpt - {link}')
                else:
                    if link not in html_str:
                        logger.warning(f'Link from gpt not valid - {link}')
                        continue
                    else:
                        logger.info(f'Link from gpt - {link}')
                
        try:
            if link.startswith("//"):
                link = 'https:' + link
            if not is_full_link(link):
                link = base_url + link

            if link.startswith('https://youtu.be/') or link.startswith('https://www.youtube.com/') :
                continue

            if not check_post_exists(db, website.owner_id, link):
                try:
                    post_text = get_post_text(link)
                    if post_text:
                        json_prompt = parse_post_prompt(post_text, website.interest[0])
                        json_post = call_chat_GPT(json_prompt, json_format=True)
                        json_post = json_post.content
                        json_post = json.loads(json_post)
                        json_post['link_to_post'] = link
                        json_post['owner_id'] = website.owner_id

                        results.append(json_post)
                except json.JSONDecodeError:
                    logger.error("The string is not properly formatted as JSON.")
                except Exception as e:
                    logger.error(e)

        except ValueError as ve:
            logger.warning(f'Error in {link}: {ve}')

    return results
    

        
