from datetime import datetime, timedelta

def format_note_date(date_obj):
    now = datetime.now()
    if date_obj > now - timedelta(days=1):
        return date_obj.strftime("%H:%M") 
    
    elif date_obj > now - timedelta(days=7):
        return date_obj.strftime("%A") 
    
    else:
        return date_obj.strftime("%d/%m/%y") 