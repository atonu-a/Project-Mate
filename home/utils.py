from django.utils import timezone

def time_ago(created_at):
    now = timezone.now()
    diff = now - created_at
    
    seconds = int(diff.total_seconds())
    if seconds<60:
        return "Just Now"
    
    minutes = seconds//60
    if minutes<60:
        return f"{minutes}m ago"
    
    hours = minutes//60
    if hours<24:
        return f"{hours}h ago"
    
    days = hours//24
    if days<7:
        return f"{days}d ago"
    
    weeks = days//7
    if weeks<4:
        return f"{weeks}w ago"
    
    return created_at.strftime("%d %b %Y")
    
    