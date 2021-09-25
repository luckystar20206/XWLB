import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pprint import pprint as pp
from XWLB.items import XwlbItem

class JdspiderSpider(CrawlSpider):
    name = 'jdSpider'
    # allowed_domains = ['www.qq.com']
    start_urls = ['http://www.fm1007.com/jdft.html']
    link1 = LinkExtractor(allow=r'com/jdft_\d+')
    link2 = LinkExtractor(restrict_xpaths='//*[@id="tab_con1"]/div/ol')
    rules = (
        Rule(link1, callback='parse_item', follow=True),
        Rule(link2, callback='parse_detail', follow=False)
    )

    def parse_item(self, response):
        pass

    def parse_detail(self, response):
        item = XwlbItem()
        title = response.xpath('//*[@id="content"]//div[@class="title"]/h2/text()').extract_first()
        txt_list = response.xpath('//*[@id="tab_con2"]/div[@class="text_content"]//p/text()').extract()
        new_txt_list = [i.strip() for i in txt_list]
        new_txt = '\n  '.join([i for i in new_txt_list if i != ''])
        item['title'] = title
        item['content'] = new_txt
        return item 