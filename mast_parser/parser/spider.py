from urllib.parse import urlparse

import scrapy
from sqlalchemy import insert, exists
from sqlalchemy.orm import sessionmaker

from mast_parser.db import engine
from mast_parser.models import FamousPerson
from mast_parser.parser.utils import (
    parse_month,
    calculate_number_of_days_in_month,
    get_search_wiki_url,
)


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Deaths_in_July_2010"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "RANDOMIZE_DOWNLOAD_DELAY": 0.5,
    }

    def parse(self, response):
        Session = sessionmaker(bind=engine)

        title = response.xpath('//h1/span[@class="mw-page-title-main"]/text()').get()

        month = parse_month(title)
        number_of_days = calculate_number_of_days_in_month(month)

        self.logger.debug(
            "Распаршен месяц %s с количеством дней %s", month, number_of_days
        )

        for day in range(1, 2):
            day_urls = response.xpath(
                f'//div[@class="mw-heading mw-heading3" and h3[@id="{day}"]]/'
                f'following-sibling::ul[1]/li/a[contains(@href, "/wiki/")][1]/@href'
            ).getall()

            self.logger.debug("Для дня %s найдено %s ссылок", day, len(day_urls))

            for url in day_urls:
                with Session() as session:
                    if session.query(
                        exists(FamousPerson).where(FamousPerson.english_url == url)
                    ).scalar():
                        self.logger.info("Статья уже есть в базе данных %s", url)

                        continue

                    yield response.follow(
                        url,
                        callback=self.parse_english_detail,
                        cb_kwargs={"english_url": url},
                    )

        self.logger.info(f'Обработана страница "{title}"')

    def parse_english_detail(self, response, english_url):
        name = response.xpath('//h1/span[@class="mw-page-title-main"]/text()').get()
        text = response.xpath(
            'string(//div[@class="mw-content-ltr mw-parser-output"]/p[not(@*)][normalize-space()][1])'
        ).get()

        search_url = get_search_wiki_url(name)

        self.logger.debug("Построен урл для поиска русской статьи %s", search_url)

        yield response.follow(
            search_url,
            callback=self.parse_search,
            cb_kwargs={
                "data": {
                    "english_url": english_url,
                    "english_name": name,
                    "english_text": text,
                }
            },
        )

        self.logger.info(f'Обработана английская статья "{name}"')

    def parse_russian_detail(self, response, data):
        name = response.xpath('//h1/span[@class="mw-page-title-main"]/text()').get()
        text = response.xpath(
            'string(//div[@class="mw-content-ltr mw-parser-output"]/p[not(@*)][normalize-space()][1])'
        ).get()

        data = {
            **data,
            "russian_name": name,
            "russian_text": text,
        }

        self.save_model(data)

        self.logger.info(f'Обработана русская статья "{name}"')

    def parse_search(self, response, data):
        pages = response.json().get("query", {}).get("pages", {})

        if len(pages) != 1:
            self.logger.error("Найдено не ровно одна страница %s", pages)

            return

        page = list(pages.values())[0]

        self.logger.debug("Найдена страница %s", page)

        langlinks = page.get("langlinks", [])

        if not langlinks:
            self.logger.warning(
                "Не найдено ни одной русской ссылки по урлу %s", response.request.url
            )
        else:
            link = langlinks[0].get("url")

            if link:
                yield response.follow(
                    link,
                    callback=self.parse_russian_detail,
                    cb_kwargs={"data": {**data, "russian_url": urlparse(link).path}},
                )

                return

        self.save_model(data)

    def save_model(self, data):
        Session = sessionmaker(bind=engine)

        with Session() as session:
            session.execute(insert(FamousPerson), [data])
            session.commit()
