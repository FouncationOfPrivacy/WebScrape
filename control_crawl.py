import scrapy
import os
import json
import shutil

class CrawlSpider(scrapy.Spider):
    name = 'control_crawl'

    def __init__(self, url=None, output_pathname=None, depth=None):
        self.count = -1
        self.depth = int(depth)
        self.output_pathname = output_pathname
        self.start_urls = [f'https://{url}']

        print(self.start_urls)

        if os.path.isdir(output_pathname):
        	shutil.rmtree(output_pathname)
        os.mkdir(output_pathname)

        self.url_collection_pathname = os.path.join(output_pathname, 'url.txt')

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = f'{page}.html'
        pathname = os.path.join(self.output_pathname, filename)

        with open(pathname, 'wb') as hdle:
            hdle.write(response.body)

        url = f'{response.url}\n'
        with open(self.url_collection_pathname, 'a+') as hdle:
            hdle.write(url)

        for href in response.xpath('//a/@href').getall():
            self.count += 1

            if self.count > self.depth:
                return

            yield scrapy.Request(response.urljoin(href), self.parse)