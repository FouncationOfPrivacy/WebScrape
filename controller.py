# python3 controller.py top_5000_sites.json 5001_to_100000_sites.json ../data

import os
import sys
import json
import shutil
import random

# 5001_to_100000_sites.json
with open(sys.argv[2], 'r') as hdle:
	urls = json.load(hdle)

urls = random.choices(urls, k=5000)

for url in urls:
	output_pathname = f'{sys.argv[3]}/{url}'
	os.system(f'scrapy runspider control_crawl.py -a url={url} -a output_pathname={output_pathname} -a depth=3')

# top_5000_sites.json
with open(sys.argv[1], 'r') as hdle:
	urls = json.load(hdle)

for url in urls:
	output_pathname = f'{sys.argv[3]}/{url}'
	os.system(f'scrapy runspider control_crawl.py -a url={url} -a output_pathname={output_pathname} -a depth=3')

# merge all url
with open(f'{sys.argv[3]}/allUrl.txt', 'a') as allUrl:
	for subdir in os.listdir(sys.argv[3]):
		path = f'{sys.argv[3]}/{subdir}/url.txt'

		if os.path.exists(path):
			with open(path, 'r') as eachUrl:
				allUrl.write(eachUrl.read())