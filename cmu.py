import scrapy
import os


class CmuSpider(scrapy.Spider):
    name = 'cmu'
    allowed_domains = ['cmu.edu']
    start_urls = ['http://cmu.edu/']

    def __init__(self):
        self.count = 0
        self.depth = 5
        self.urls = os.path.join(CmuSpider.name, 'urls.txt')

    def parse(self, response):

        if self.count == self.depth:
            return

        page = response.url.split('/')[-2]
        filename = f'{page}.html'
        pathname = os.path.join(CmuSpider.name, filename)

        with open(pathname, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {pathname}')

        url = f'{response.url}\n'
        with open(self.urls, 'a+') as f:
            f.write(url)

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)

        self.count += 1
