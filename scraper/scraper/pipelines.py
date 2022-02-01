# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from bs4 import BeautifulSoup


class ScraperPipeline:
    def process_item(self, item, spider):
        if item['date']:
            item.save()
        return item
class DescriptionPipeline:
    def process_item(self, item, spider):
        li = item['description']
        item['description'] = ''
        for x in li:
            s = BeautifulSoup(x, features= 'html.parser')
            item['description'] =item['description'] + ' ' +s.getText(separator=' ') 
        return item
