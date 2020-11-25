# execute command as following:
# python3 controller.py top_5000_sites.json 5001_to_100000_sites.json ../data

import os
import sys
import json
import shutil
import random
import argparse


def run_scrapy(seeds, output):
    for url in seeds:
        output_pathname = os.path.join(output, url)
        os.system(f'scrapy runspider control_crawl.py'
                    f' -a url={url}'
                    f' -a output_pathname={output_pathname}'
                    f' -a depth=3')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_segment')
    parser.add_argument('--index')
    parser.add_argument('--seed')
    parser.add_argument('--output')

    args = parser.parse_args()
    if not args.num_segment or not args.index or not args.seed or not args.output:
        parser.print_help()
        return

    index = int(args.index)
    num_segment = int(args.num_segment)
    seeds = []
    with open(args.seed, 'r') as hdle:
        seeds = json.load(hdle)

    total = len(seeds)
    size_segment = int(total / num_segment)
    begin = index * size_segment
    end = begin + size_segment
    seeds_segment = seeds[begin:end]

    run_scrapy(seeds_segment, args.output)


if __name__ == '__main__':
    main()

