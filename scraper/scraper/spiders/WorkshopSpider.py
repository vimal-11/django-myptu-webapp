from unicodedata import category
import scrapy
from scraper.items import WorkshopItem
from workshops.models import Workshop
class WorkshopSpider(scrapy.Spider):
    name = "WorkshopSpider"
    start_urls = ["https://www.eventbrite.com/d/online/science-and-tech--events/hackathon/?page=1"]
    def parse(self, response):
        for i in range(5):
           req = '''https://www.eventbrite.com/d/online/science-and-tech--events/hackathon/?page=''' + str((i+1))
           yield scrapy.Request(url = req, callback = self.parse_pages)
    def parse_pages(self, response):
        for x in range(20):
            r = response.xpath( '''/html/body/div[2]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[1]/div/ul/li['''+str((x+1))+''']/div/div/div[2]/div/div/div/article/div[1]/div/div/div[1]/a/@href''').extract()
            yield scrapy.Request(url = r[0], callback = self.parse_topic)
    def parse_topic(self, response):
        item = WorkshopItem()
        item['category'] = "Science and Tech"
        item['price'] = (response.xpath('''/html/body/main/div[1]/div[4]/div/div[1]/div/div[2]/div/div[3]/div/text()''').extract())[0]
        item['workshop_title'] = (response.xpath('''/html/body/main/div[1]/div[4]/div/div[1]/div/div[2]/div/div[2]/h1/text()''').extract())[0]
        item['description'] = response.xpath("/html/body/main/div[1]/div[4]/div/section[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/div").extract()
        item['date'] = ''
        for i in range(2):
            try:
                k = response.xpath('''/html/body/main/div[1]/div[4]/div/section[1]/div[1]/div/div/div[2]/div/div[1]/time/p[''' +str(i+1)+''']/text()''').extract()[0]
                item['date'] = item['date']+ ' '+k
            except:
                item['date']=item['date']+''
        return item
