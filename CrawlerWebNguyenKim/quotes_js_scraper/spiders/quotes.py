import json
import math
import scrapy
from quotes_js_scraper.items import QuoteItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode

class WebCrawlerSpider(scrapy.Spider):
    name = 'NguyenKimCrawler'

    def start_requests(self):
        crawler_search_url = 'https://www.nguyenkim.com/laptop-may-tinh-xach-tay/page-4/'
        yield SeleniumRequest(url=crawler_search_url, callback=self.parse_search_results, wait_time=30, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '#pagination_contents > script')))

    def parse_search_results(self, response):
        # page = response.meta['trang']
        # keyword = response.meta['keyword']
        products = response.css('#pagination_contents > script::text').getall()
        # products = json.loads(products) 
        # print(products[0])
        for i in range(26):
            # product = json.loads(product)
            # crawler_product_url = product['offers']['url']
            # print(response.css(f'#pagination_contents > a').get())
            item = json.loads(products[i])
            # print(item)
            yield {
                'Url': item['offers']['url'],
                'Name': item['name'],
                'Price': item['offers']['price']
            }
            # yield SeleniumRequest(url=crawler_product_url, callback=self.parse_product_data, wait_time=10, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '#root > script:nth-child(4)')), meta={'url': crawler_product_url})

            # # Request Next Page
            # if page == 1:
            #     max_pages = json_blob["props"]["initialState"]["catalog"]["paging"]["last_page"]
            #     # if max_pages > 10:
            #     #     max_pages = 10
            #     for p in range(2, 5):
            #         payload = {'sort': 'newest', 'page': p}
            #         crawler_search_url = 'https://tiki.vn/' + keyword + '?' + urlencode(payload)
            #         yield SeleniumRequest(url=crawler_search_url, callback=self.parse_search_results, wait_time=0.5, meta={'keyword': keyword, 'page': p})

    def parse_product_data(self, response):
        detail_product = json.loads(response.css('#root > script:nth-child(4)::text').get())
        # print(detail_product['additionalProperty'][8]['value'])
        yield {
            'Name': detail_product['name'],
            'Price': findPrice(detail_product['offers']),
            'Brand': detail_product['brand']['name'],
            'Url': response.meta['url'],
            'Rated': detail_product['aggregateRating']['ratingValue'],
            'Votes': detail_product['aggregateRating']['reviewCount'],
            'Imgs': response.css('#root > main > div > div.l-pd-header > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-left > div.st-slider > div > div.swiper-wrapper.js--slide--full > div > img::attr(src)').getall(),
            'CPU': str(next(sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'CPU')),
            'RAM': str(next(sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'RAM')),
            'ManHinh': str(next(sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'Màn hình')),
            'OCung': str(next(sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'Ổ cứng')),
            'Card': str(next(sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'Đồ họa')),
            'HDH': str(next(sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'Hệ điều hành')),
            'KT&KL': ', '.join([sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'Kích thước'] + [sub['value'] for sub in detail_product['additionalProperty'] if sub['name'] == 'Trọng lượng'])
        }

# scrapy crawl NguyenKimCrawler -o outputFull.json