# web_scraping-crawling_samples
A repository contains a mixture of samples for scraping & crawling with scrapy, selenium and Lua.

### fake_bookstore_scrapy
A pipeline that crawls a fake bookstore website and saves the data into local MySQL database.

To create a new scrapy project:
```commandline
scrapy startproject <new_project_name>
scrapy genspider <new_crawler_name> -t crawl <url_to_scrape>
```
For running existing one:
```commandline
poetry install
poetry shell
scrapy crawl bookstore_crawler
```
