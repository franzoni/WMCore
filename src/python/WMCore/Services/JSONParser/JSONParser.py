#!/usr/bin/env python
"""
_JSONParser_

API for parsing JSON URLs and returning as python objects.

"""

__revision__ = "$Id: JSONParser.py,v 1.4 2008/10/15 13:47:25 ewv Exp $"
__version__ = "$Revision: 1.4 $"

import urllib
import cStringIO
import tokenize
import logging

from WMCore.Services.Service import Service

class JSONParser:
    """
    API for dealing with retrieving information from SiteDB
    """

    def __init__(self, url, logger = None):
        if not logger:
            logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/WMCoreJSONparser.log',
                    filemode='w')
            logger = logging.getLogger('JSONParser')
        dict = {}
        dict['endpoint'] = url
        dict['cachepath'] = '/tmp/jsonparser'
        dict['type'] = 'text/json'
        dict['logger'] = logger
        self.service = Service(dict)

    def getJSON(self, service, file='result.json', **args):
        """
        _getJSON_

        retrieve JSON formatted information given the service name and the
        argument dictionaries

        """
        params = urllib.urlencode(args)
        query = service + '?' + params

        try:
            f = self.service.refreshCache(file, query)
            #f = urllib.urlopen(service, params)
            result = f.read()
            f.close()
        except IOError:
            raise RuntimeError("URL not available: %s" % service )

        output = self.dictParser(result)
        return output


    def parse(self, token, src):
        """
        Dictionary string parser from
        Fredrik Lundh (fredrik at pythonware.com)
        on python-list
        """
        if token[1] == "{":
            out = {}
            token = src.next()
            while token[1] != "}":
                key = self.parse(token, src)
                token = src.next()
                if token[1] != ":":
                    raise SyntaxError("Malformed dictionary")
                value = self.parse(src.next(), src)
                out[key] = value
                token = src.next()
                if token[1] == ",":
                    token = src.next()
            return out
        elif token[1] == "[":
            out = []
            token = src.next()
            while token[1] != "]":
                out.append(self.parse(token, src))
                token = src.next()
                if token[1] == ",":
                    token = src.next()
            return out
        elif token[0] == tokenize.STRING:
            return token[1][1:-1].decode("string-escape")
        elif token[0] == tokenize.NUMBER:
            try:
                return int(token[1], 0)
            except ValueError:
                return float(token[1])
        else:
            print "Bad token", token
            raise SyntaxError("Malformed expression")


    def dictParser(self, source):
        """
        Dictionary string parser from
        Fredrik Lundh (fredrik at pythonware.com)
        on python-list
        """
        src = cStringIO.StringIO(source).readline
        src = tokenize.generate_tokens(src)
        return self.parse(src.next(), src)
