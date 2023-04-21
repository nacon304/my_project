import json
import math
import scrapy
from quotes_js_scraper.items import QuoteItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode

class WebCrawlerSpider(scrapy.Spider):
    name = 'FPTCrawler'

    def start_requests(self):
        keyword_list = ['may-tinh-xach-tay']
        for keyword in keyword_list:
            payload = {'sort': 'ban-chay-nhat', 'trang': 9}
            crawler_search_url = 'https://fptshop.com.vn/' + keyword + '?' + urlencode(payload)
            yield SeleniumRequest(url=crawler_search_url, callback=self.parse_search_results, wait_time=60, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, "#plistppromotion44278")), meta={'keyword': keyword,'trang': 1})

    def parse_search_results(self, response):
        page = response.meta['trang']
        keyword = response.meta['keyword']
        script_tag  = response.css('head > script[data-react-helmet="true"]').get()

        script_tag = script_tag[script_tag.find('[') : script_tag.rfind(']') + 1]

        if script_tag is not None:
            product_list = json.loads(script_tag)
            for product in product_list:
                url = response.css(f'a[title="{product["item_name"]}"]::attr(href)').get()
                crawler_product_url = 'https://fptshop.com.vn' + url
                yield SeleniumRequest(url=crawler_product_url, callback=self.parse_product_data, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'st-pd-table')), meta={'keyword': keyword, 'trang': page, 'product': product, 'url': crawler_product_url})

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
        detail = sorted(detail_product['additionalProperty'], key=lambda d: d['name']) 
        # print(detail_product['additionalProperty'][8]['value'])
        yield {
            'Name': response.meta['product']['item_name'],
            'OriginalPrice': response.meta['product']['price'],
            'Price': response.meta['product']['price'] - response.meta['product']['discount'],
            'Brand': response.meta['product']['item_brand'],
            'Url': response.meta['url'],
            'Imgs': response.css('#root > main > div > div.l-pd-header > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-left > div.st-slider > div > div.swiper-wrapper.js--slide--full > div > img::attr(src)').getall(),
            'CPU': detail[0]['value'],
            'RAM': detail[5]['value'],
            'ManHinh': detail[3]['value'],
            'OCung': detail[9]['value'],
            'Card': detail[8]['value'],
            'HDH': detail[1]['value'],
            'KT&KL': detail[2]['value'] + ", " + detail[6]['value']
        }

# scrapy crawl FPTCrawler -o outputFull.json