# import scrapy
# from quotes_js_scraper.items import QuoteItem


# class QuotesSpider(scrapy.Spider):
#     name = 'quotes'
#     allowed_domains = ['quotes.toscrape.com']
#     start_urls = ['http://quotes.toscrape.com/']

#     def parse(self, response):
#         pass

## spider.py
import json
import math
import scrapy
from quotes_js_scraper.items import QuoteItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode

class WebCrawlerSpider(scrapy.Spider):
    name = 'TikiCrawler'

    def start_requests(self):
        # 'laptop/c8095'
        # 'ram-may-tinh/c2680'
        # 'o-cung-gan-trong/c28844'
        # 'man-hinh-may-tinh/c2665'
        # 'ban-phim-choi-game/c5267'
        # 'chuot-choi-game/c3428'
        keyword_list = ['chuot-choi-game/c3428']
        for keyword in keyword_list:
            payload = {'sort': 'newest', 'page': 1}
            crawler_search_url = 'https://tiki.vn/' + keyword + '?' + urlencode(payload)
            yield SeleniumRequest(url=crawler_search_url, callback=self.parse_search_results, wait_time=0.5, meta={'keyword': keyword,'page': 1})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword']
        script_tag  = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        if script_tag is not None:
            json_blob = json.loads(script_tag)

            product_list = json_blob["props"]["initialState"]["catalog"]["data"]
            for product in product_list:
                crawler_product_url = 'https://tiki.vn/' + product.get('url_path', '')
                yield scrapy.Request(url=crawler_product_url, callback=self.parse_product_data, meta={'keyword': keyword, 'page': page, 'product': product, 'url': crawler_product_url})

            # Request Next Page
            if page == 1:
                max_pages = json_blob["props"]["initialState"]["catalog"]["paging"]["last_page"]
                # if max_pages > 10:
                #     max_pages = 10
                for p in range(2, 5):
                    payload = {'sort': 'newest', 'page': p}
                    crawler_search_url = 'https://tiki.vn/' + keyword + '?' + urlencode(payload)
                    yield SeleniumRequest(url=crawler_search_url, callback=self.parse_search_results, wait_time=0.5, meta={'keyword': keyword, 'page': p})

    def parse_product_data(self, response):
        yield {
            'Name': response.meta['product']['name'],
            'Price': response.meta['product']['price'],
            'Imgs': response.css("#__next > div:nth-child(1) > main > div.Container-sc-itwfbd-0.hfMLFx > div.styles__Wrapper-sc-8ftkqd-0.eypWKn > div.style__ProductImagesStyle-sc-1fmads3-0.fymfgs > div.review-images > div picture img ::attr(src)").getall(),
            'url': response.meta['url']
        }

# scrapy crawl TikiCrawler -o output3.json
# JSON.parse(window.document.querySelectorAll("#pagination_contents > script")[0].innerHTML)