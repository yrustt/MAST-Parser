import time

import schedule
import daemon

from mast_parser.tasks import scrape, notify
from mast_parser import settings


def main():
    with daemon.DaemonContext(
        stdout=open("stdout.log", "a+"),
        stderr=open("stderr.log", "a+"),
        working_directory=settings.BASE_DIR,
    ):
        schedule.every().day.at("01:00").do(scrape)
        schedule.every().day.at("12:00").do(notify)

        while True:
            print(f"Time {time.time()}")
            schedule.run_pending()
            time.sleep(60)


if __name__ == "__main__":
    main()
