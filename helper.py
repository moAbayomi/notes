from datetime import datetime, timedelta
import re
from markupsafe import Markup

def format_note_date(date_obj):
    now = datetime.now()
    if date_obj > now - timedelta(days=1):
        return date_obj.strftime("%H:%M") 
    
    elif date_obj > now - timedelta(days=7):
        return date_obj.strftime("%A") 
    
    else:
        return date_obj.strftime("%d/%m/%y") 
    
def highlighter(text, query):
    if not query:
        return Markup.escape(text)
    
    highlightd = re.sub(f"({re.escape(query)})", r'<mark class="bg-yellow-300 px-0.5 rounded-sm">\1</mark>', 
        text, flags=re.IGNORECASE)
    return Markup(highlightd)