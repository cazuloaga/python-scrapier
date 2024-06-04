from bs4 import BeautifulSoup

def extract_href(html_soup: BeautifulSoup):
    """
    Extracts unique href attribute values from anchor <a> tags in HTML content.

    Parameters:
    - html_soup (BeautifulSoup): A BeautifulSoup object containing HTML content from the alerts.

    Returns:
    - results (list): A list of unique href attribute values found in the HTML content.
    """

    # Initializing an empty list to store the extracted href values
    results = []

    # Looping through all anchor tags in the HTML content
    for a in html_soup.find_all('a', href=True):
        # Checking if the href attribute is present and not already in the results list
        if a['href'] not in results:
            # Adding the href value to the results list if it meets the condition
            results.append(a['href'])

    # Returning the list of unique href values
    return results