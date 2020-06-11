#!/usr/bin/python

import argparse
from datetime import datetime

from pyparsing import Word, alphas, Suppress, Combine, nums, string, Regex, Optional, ParseException


# syslog format reference:
# https://tools.ietf.org/html/rfc5424
class Parser(object):
    """ A parser for syslog lines """

    def __init__(self):
        number = Word(nums)  # meta var to use in parsing futher 

        # parse the date and convert it to datetime
        month = Word(string.ascii_uppercase, string.ascii_lowercase, exact=3) 
        day   = number
        hour  = Combine(number + ":" + number + ":" + number)
        timestamp = month + day + hour
        timestamp.setParseAction(lambda x: datetime.strptime(
            '{} {}'.format(datetime.now().year, ' '.join(x)),
            '%Y %b %d %H:%M:%S'
        ))

        # parse hostname
        hostname = Word(alphas + nums + "_-.")

        # parse application name
        app = Word(alphas + "/-_.()")("app") + (Suppress("[") + number("pid") + Suppress("]")) | (Word(alphas + "/-_.")("app"))

        # parse message (rest of the line)
        message = Regex(".*")

        # pattern to parse and field names
        self._pattern = timestamp("timestamp") + hostname("hostname") + Optional(app) + Suppress(':') + message("message")

    def parse(self, line):
        parsed = self._pattern.parseString(line)
        # fill in keys that might not have been found in the input string
        for key in ['app', 'pid']:
            if key not in parsed:
                parsed[key] = ''
        return parsed.asDict()


def parse_args():
    """ Parse cmd arguments """
    parser = argparse.ArgumentParser(description='The script writes Fibonacci numbers to file')
    parser.add_argument('--path', type=str, default='/var/log/syslog',
            help='a string - path to syslog file')
    parser.add_argument('--type', type=str, default='app',
            help='a string - type of summarize, per "minute" or "app" (default: app)')
    parser.add_argument('--skip', action='store_true',
            help='a flag to skip incorrect lines of syslog file')
    args = parser.parse_args()
    return args


def main():
    """ Main logic of the script: parse arguments, open file and summarize events 
    In this script, we read syslog file, summarize all events per 'type' and after print the result.

    TODO: with 'minute' summarize type we can summarize and print the result in stream,
    without waiting till the end of the file.
    """

    try:
        args = parse_args()
        if args.type not in ['app', 'minute']:  # check the args
            print('Error! Unknown summarize type. Use "app" or "minute" instead.')
            exit(1)

        parser = Parser()
        summary_dict = {}
        max_len = 0
        try:
            with open(args.path) as syslog_file:
                for i, line in enumerate(syslog_file):
                    try:
                        fields = parser.parse(line)  # parse fields of the line
                    except ParseException:
                        if not args.skip:
                            print('Error! Incorrect syslog format at line {}'.format(i+1))
                            exit(1)

                    if args.type == 'app':
                        key = fields['app']
                    else:
                        key = fields['timestamp'].isoformat(timespec='minutes')

                    if key not in summary_dict:
                        summary_dict[key] = 1
                        if len(key) > max_len:
                            max_len = len(key)
                    else:
                        summary_dict[key] += 1
        except IOError:
            print('Error! Can not open the file {}. Are the path and the access mode correct?'.format(args.path))
            exit(1)

        # separated from the main loop to show the final result of summarization
        # create a table with header
        header = '{name: <{width}}   {count}'.format(name=args.type, width=max_len, count='events')
        print(header)
        print('-' * len(header))
        for name, count in summary_dict.items():
            print('{name: <{width}}   {count}'.format(name=name, width=max_len, count=count))

    except KeyboardInterrupt:
        print('Exit from keyboard')


if __name__ == "__main__":
    main()
