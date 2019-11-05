

hour_format = "HH:mm:ss"
date_format = "DD/MM/YYYY"

def format_date(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    str = '{:}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
    return (str)
