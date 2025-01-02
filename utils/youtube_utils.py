# utils/youtube_utils.py

import re

def extract_youtube_video_id(url):
    """
    Extract the YouTube video ID from a URL.
    
    Args:
        url (str): The YouTube URL.
        
    Returns:
        str or None: The extracted video ID if found, else None.
    """
    regex = (
        r'(?:v=|\/|embed\/|youtu\.be\/|v\/|watch\?v=)'
        r'([0-9A-Za-z_-]{11})'
    )
    match = re.search(regex, url)
    return match.group(1) if match else None
