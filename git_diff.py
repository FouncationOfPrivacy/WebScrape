from pydriller import RepositoryMining

import argparse
import os
import datetime
import json


def should_ignore(line):
    return line.startswith('@@') or \
            line.startswith('##') or \
            '#?#' in line or \
            '#@#' in line


def parse_by_date(repo, bgn, end):
    lines = []

    miner = RepositoryMining(repo, since=bgn, to=end)
    for commit in miner.traverse_commits():
        for modification in commit.modifications:
            added = modification.diff_parsed['added']
            for item in added:
                line = item[1]
                if should_ignore(line):
                    continue
                lines.append(line)

    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo')
    parser.add_argument('--output')

    args = parser.parse_args()
    if not args.repo or not args.output:
        parser.print_help()
        return

    dates = []
    for i in range(1, 30):
        dates.append(i)

    report = {}

    for date in dates:
        begin = datetime.datetime(2020, 11, date, 0, 0)
        end = datetime.datetime(2020, 11, date, 23, 59)
        print(f'Process {date}th day...')
        lines = parse_by_date(args.repo, begin, end)

        path = os.path.join(args.output, f'{date}th')
        with open(path, 'w') as hdle:
            for line in lines:
                out_line = f'{line}\n'
                hdle.write(out_line)

        report[date] = len(lines)

    path = os.path.join(args.output, 'report.json')
    with open(path, 'w') as hdle:
        json.dump(report, hdle)


if __name__ == "__main__":
    main()

