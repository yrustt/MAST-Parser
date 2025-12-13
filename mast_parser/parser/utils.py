from datetime import datetime
from urllib.parse import urlencode

from dateutil.relativedelta import relativedelta


def parse_month(date_str):
    return datetime.strptime(date_str, "Deaths in %B %Y").date()


def calculate_number_of_days_in_month(month):
    next_month = month + relativedelta(months=1)

    return (next_month - month).days


def get_search_wiki_url(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "lllang": "ru",
        "lllimit": 1,
        "llprop": "url",
        "prop": "langlinks",
        "titles": title,
    }
    encoded_params = urlencode(params)

    return f"{url}?{encoded_params}"
