import subprocess
import sys

from mast_parser import settings


def scrape(month: str | None = None):
    """
    :param month: В формате YYYY-MM
    :return:
    """

    command = [
        "scrapy",
        "runspider",
        settings.SPIDER_MODULE,
    ]

    if month:
        command.extend(["-a", f"start_month={month}"])

    subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, check=True)
