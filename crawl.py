import scrapy
import os
import json
import shutil


class CrawlSpider(scrapy.Spider):
    name = 'crawl'

    def __init__(self, seeds_pathname=None, output_pathname=None, depth=None):

        if seeds_pathname is None or output_pathname is None or depth is None:
            print('\n\nscrapy runspider crawl.py '
                    '-a seeds_pathname=example.json '
                    '-a output_pathname=./example '
                    '-a depth=3\n\n')
            return

        self.count = 0
        self.depth = int(depth)
        self.output_pathname = output_pathname
        self.start_urls = []

        with open(seeds_pathname, 'r') as hdle:
            urls = json.load(hdle)
            for url in urls:
                self.start_urls.append(f'https://{url}')

        print(self.start_urls)

        if os.path.isdir(output_pathname):
            shutil.rmtree(output_pathname)
        os.mkdir(output_pathname)

        self.url_collection_pathname = os.path.join(output_pathname, 'url.txt')

    def parse(self, response):

        if self.count == self.depth:
            return

        page = response.url.split('/')[-2]
        filename = f'{page}.html'
        pathname = os.path.join(self.output_pathname, filename)

        with open(pathname, 'wb') as hdle:
            hdle.write(response.body)

        url = f'{response.url}\n'
        with open(self.url_collection_pathname, 'a+') as hdle:
            hdle.write(url)

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)

        self.count += 1
