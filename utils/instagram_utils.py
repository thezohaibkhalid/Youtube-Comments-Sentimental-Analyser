import re

def extract_instagram_shortcode(url):
    """
    Extract the Instagram shortcode from a URL.
    
    Args:
        url (str): The Instagram post URL.
        
    Returns:
        str or None: The extracted shortcode if found, else None.
    """
    regex = r"/p/([a-zA-Z0-9_-]+)/"
    match = re.search(regex, url)
    return match.group(1) if match else None
