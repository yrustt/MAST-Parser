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


def clean_russian_text(text):
    no_accent = [
        "а",
        "я",
        "у",
        "ю",
        "о",
        "е",
        "э",
        "и",
        "ы",
        "А",
        "Я",
        "У",
        "Ю",
        "О",
        "Е",
        "Э",
        "И",
    ]
    accented = [
        "а́",
        "я́",
        "у́",
        "ю́",
        "о́",
        "е́",
        "э́",
        "и́",
        "ы́",
        "А́",
        "Я́",
        "У́",
        "Ю́",
        "О́",
        "Е́",
        "Э́",
        "И́",
    ]
    trans_table = dict(zip(accented, no_accent))

    return text.translate(trans_table)
