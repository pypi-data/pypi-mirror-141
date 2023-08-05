#!/usr/bin/python3

"""
This program is a client to dpaste.de service which enables the user to paste console output.
Created by Lukas Ruzicka (lruzicka@redhat.com), 2019.

This program is under the GPLv3 license. You may use it accordingly.
"""

import sys
import argparse
import requests

class Parser:
    """ This class is the argument parser.  """
    def __init__(self):
        """ Initialize parser """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-f', '--file', default='empty', help='Input a file and paste the content.')
        self.parser.add_argument('-l', '--lexer', default='_text', help='Type of content - used for formatting.')
        self.parser.add_argument('-e', '--expire', default='hour', help='How long to keep the snippet online.')
        self.parser.add_argument('-c', '--content', default='empty', help='A content to be pasted to the webpage')

    def provide_arguments(self, args=None):
        """ Return arguments from the parser """
        arguments = self.parser.parse_args(args)
        return arguments

class Dpaster:
    """ This class is the application functionality """
    def __init__(self, api, arguments):
        """ Initialize the application Dpaste """
        self.api = api
        self.args = arguments
        self.expiry = arguments.expire 
        self.lexer = arguments.lexer
        self.file = None
        self.content = None
        self.jsondata = None

    def convert_time(self):
        """ Converts human readable times to corresponding values in seconds. """
        if self.args.expire == 'hour':
            self.expiry = 3600
        elif self.args.expire == 'day':
            self.expiry = 3600 * 24
        elif self.args.expire == 'week':
            self.expiry = 3600 * 24 * 7
        elif self.args.expire == 'month':
            self.expiry = 3600 * 24 * 30
        elif self.args.expire == 'never':
            self.expiry = 'never'
        else:
            self.expiry = 'onetime'
        return self.expiry

    def get_paste(self):
        """ Collect and return the paste content """
        # Get content to paste
        # If content taken from a file:
        if self.args.file != 'empty':
            with open(self.args.file) as infile:
                lines = infile.readlines()
            self.content = "".join(lines)

        # If provided on CLI
        elif self.args.content != 'empty':
            self.content = self.args.content

        # If provided by pipe
        elif sys.stdin:
            lines = [line for line in sys.stdin]
            self.content = "".join(lines)

        # If not provided at all
        else:
            self.content = "The user has not selected anything clever to paste, so we pasted this warning."
            print("You have not selected anything to paste")
        return self.content

    def prepare_paste(self):
        """ Return the json content for the http request """
        self.jsondata = {
            'format': 'url',
            'lexer': self.lexer,
            'expires': self.expiry,
            'content': self.content,
        }
        return self.jsondata


    def send_to_api(self):
        """ Make the http request to the server """
        process = requests.post(self.api, data=self.jsondata)
        if process.status_code == 200:
            print(process.content.decode("utf-8"))
        else:
            print("Something went wrong, the content was not copied.")
            print(process.status_code)

def main():
    """ Main program body """
    argparser = Parser()
    args = argparser.provide_arguments()

    application = Dpaster('https://dpaste.org/api/', args)

    # Calculate time in seconds to replace keywords.
    application.convert_time()

    application.get_paste()

    # Prepare data for API connection
    application.prepare_paste()

    # Connect with API
    application.send_to_api()


if __name__ == "__main__":
    main()
