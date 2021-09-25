# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import datetime

class XwlbPipeline:
    def __init__(self): 
        fp = None
        box = None
    def open_spider(self,spider):
        print('爬虫开始')
        self.box = dict() 

    def process_item(self, item, spider):
        if spider.name == 'xwSpider':
            num = re.findall('(\d+?)年(\d+?)月(\d+?)日',item['title'])
            t = datetime.date(int(num[0][0]),int(num[0][1]),int(num[0][2]))
            self.box[t] = item['content']
        else:
            num = re.findall(' \d+? ',item['title'])[0]
            t = int(num)
            self.box[t] =(item['title'],item['content'])
        return item

    def close_spider(self,spider):
        my_day = str(datetime.date.today())
        if spider.name == 'xwSpider':
            file_path = './新闻联播新闻联播文字摘要版_截至'+my_day+'.txt'
            with open(file_path, 'w', encoding='utf-8') as f:
                for i in sorted(self.box,reverse=True):
                    f.write(str(i)+' 新闻联播文字摘要版\n'+'**************\n'+self.box[i]+'\n#################\n\n\n\n\n')
        else:
            file_path = './焦点访谈_截至'+my_day+'.txt'
            with open(file_path, 'w', encoding='utf-8') as f:
                for i in sorted(self.box,reverse=True):
                    f.write(self.box[i][0]+'\n**************\n  '+self.box[i][1]+'\n#################\n\n\n\n\n')
        print('爬虫结束')
