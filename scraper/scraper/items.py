# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from workshops.models import Workshop

class WorkshopItem(DjangoItem):
    django_model = Workshop
