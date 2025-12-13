import subprocess
import sys


def scrape(month: str | None = None):
    """
    :param month: В формате YYYY-MM
    :return:
    """

    command = [
        "scrapy",
        "runspider",
        "./parser/spider.py",
    ]

    if month:
        command.extend([
            "-a",
            f"start_month={month}"
        ])

    result = subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr)

    print(result.returncode)
    print(result.stderr)
