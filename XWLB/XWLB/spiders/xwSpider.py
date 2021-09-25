import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from XWLB.items import XwlbItem

class XwspiderSpider(CrawlSpider):
    name = 'xwSpider'
    # allowed_domains = ['www.xw.com']
    start_urls = ['http://www.ab3.com.cn/cctv.html']
    link1 = LinkExtractor(allow=r'cn/cctv_\d+')
    link2 = LinkExtractor(restrict_xpaths='//*[@id="page-news-list"]/div[1]/div[2]/ul')
    rules = (
        Rule(link1, callback='parse_item', follow=True),
        Rule(link2, callback='parse_detail', follow=False)
    )

    def parse_item(self, response):
        pass

    def parse_detail(self, response):
        item = XwlbItem()
        title = response.xpath('//div[@class="content-title"]/h1/text()').extract_first()
        txt = response.xpath('//div[@class="content-txt"]/text()').extract()
        txt_list = [i.strip() for i in txt]
        new_txt = '\n'.join([i for i in txt_list if i != ''])
        item['title'] = title
        item['content'] = new_txt
        return item 
