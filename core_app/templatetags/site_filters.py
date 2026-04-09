from django import template
import re
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter(name='yt_id')
def yt_id(url):
    if not url:
        return ''
    if len(url) == 11 and '/' not in url and '.' not in url:
        return url
    
    # Try parsing as URL
    try:
        parsed = urlparse(url)
        if 'youtube.com' in parsed.netloc:
            # Check for query param 'v'
            qs = parse_qs(parsed.query)
            if 'v' in qs:
                return qs['v'][0]
            # Check for embed path /embed/ID
            path_parts = parsed.path.split('/')
            if 'embed' in path_parts:
                return path_parts[path_parts.index('embed') + 1]
            return path_parts[-1]
        if 'youtu.be' in parsed.netloc:
            return parsed.path.strip('/')
    except:
        pass
    
    # Fallback to Regex
    regex = r'(?:v=|\/embed\/|\/v\/|youtu\.be\/|\/watch\?v=|\&v=)([^#\&\?]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    
    return url
