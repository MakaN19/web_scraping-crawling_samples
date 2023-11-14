import logging

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


logging.getLogger("__main__")
logging.basicConfig(level=logging.INFO)


class BookstoreCrawlerSpider(CrawlSpider):
    name: str = "bookstore_crawler"
    allowed_domains: list[str] = ["books.toscrape.com"]
    user_agent: str = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/119.0.0.0afari/537.36")

    rules: tuple = (Rule(LinkExtractor(restrict_xpaths=r"//article[@class='product_pod']/h3/a"),
                          callback="parse_item", follow=True),
                    Rule(LinkExtractor(restrict_xpaths=r"//li[@class='next']/a"), follow=True))

    def start_requests(self) -> None:
        yield scrapy.Request(url="https://books.toscrape.com",
                             headers={"user-agent": self.user_agent})

    def set_user_agent(self, request: scrapy.http.Request) -> None:
        request.headers["User-Agent"] = self.user_agent

    def parse_item(self, response: scrapy.http.Response) -> dict[str, str]:
        main = response.xpath("//div[contains(@class, 'product_main')]")
        title = main.xpath("./h1/text()").get()
        price = main.xpath("./p[@class='price_color']/text()").get()

        return {
            "title": title,
            "price": price
        }
