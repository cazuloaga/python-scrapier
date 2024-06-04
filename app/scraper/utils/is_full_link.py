import re

def is_full_link(link: str) -> bool:
    """
    Check if a given link is a full link (absolute URL) or a relative link.
    A full link usually starts with 'http://' or 'https://'.
    """
    return bool(re.match(r'^https?:\/\/', link))