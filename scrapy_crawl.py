import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class MySpider(CrawlSpider):
    name = 'crawlspider'
    allowed_domains = ['mygov.scot']
    start_urls = ['https://www.mygov.scot/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = dict()
        item['url'] = response.url
        item['title']=response.xpath('//title').extract_first()
        item['possible-long-dates']=re.findall(r'(\d+ \w+ 20[012][0-9])', response.body)
        item['possible-long-dates-incorrect-format']=re.findall(r'(\d+\w+ \w+ 20[012][0-9])', response.body)
        item['possible-short-dates']=re.findall(r'(\d+\/\d+\/\d+)', response.body)
        item['possible-short-financial-year-dates']=re.findall(r'(20[012][0-9]\/[012][0-9])', response.body)
        item['possible-short-financial-year-incorrect-dates']=re.findall(r'(20[012][0-9]-[012][0-9])', response.body)
        item['possible-long-financial-year-dates']=re.findall(r'(20[012][0-9]\/20[012][0-9])', response.body)
        item['possible-year']=re.findall(r'(20[012][0-9])', response.body)
        return item
