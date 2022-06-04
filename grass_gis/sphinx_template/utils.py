# -- GISMentors subroutines --------------------------------------
import datetime
import locale

def get_month_year(force_locale='en_US.UTF-8'):
    locale.setlocale(locale.LC_ALL, force_locale)
    from calendar import month_name
    
    date = datetime.datetime.now()
    s = month_name[date.month]
    return s, date.year

def get_year():
    date = datetime.datetime.now()
    return date.year
