from __future__ import absolute_import

import csv
import logging
import os
import re

from project_runpy import ColorizingStreamHandler
# from utils.handlers import JSONFileHandler

from .models import Variable

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(ColorizingStreamHandler())
logfile = os.environ.get('THEDP_IMPORT_LOGFILE')
if logfile:
    pass
    # TODO
    # logger.addHandler(JSONFileHandler(logfile))


class IpedsCSVReader(object):
    """
    A special CSV reader for IPEDS reports.

    TODO remove Django model dependency.

    temp instructions for now
    run IpedsCsvReader, then parse_rows
    """
    header = None
    header_parsed = None

    def __init__(self, fh, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._reader = self.get_reader(fh)
        self.parse_header()

    def get_reader(self, fh):
        return csv.reader(fh)

    def parse_header(self):
        """
        Extract information about what variables are in the CSV.
        """
        header = self._reader.next()
        self.header = header
        header_parsed = [None for __ in header]
        # the first two columns are the institution id and name
        for idx, cell in enumerate(header):
            if idx < 2:
                header_parsed[idx] = cell
                continue
            # DELETEME this is just a hack to get around the last empty col
            if not cell:
                continue
            short_name, raw_code = re.match(r'([A-Z0-9]+)\s\((\w+)\)', cell).groups()
            # XXX begin copy pasted from models.py
            butts = re.match(r'(DRV)?([a-zA-Z]+)(\d{4})', raw_code).groups()
            __, code, year = butts
            if int(year[:2]) == int(year[2:]) - 1:
                # I've only found post Y2K years this has happened
                year = u'20' + year[:2]
            # XXX end
            header_parsed[idx] = short_name, year, raw_code
        self.header_parsed = header_parsed

    def __iter__(self):
        """
        Do stuff.
        """
        assert self.header_parsed is not None
        for row in self._reader:
            yield zip(self.header_parsed, row)

    def explain_header(self):
        """
        Explain what header information was extracted.
        """
        name_set = set()
        for cell in self.header:
            try:
                name, code = re.match(r'(\w+)\((\w+)\)', cell).groups()
                var = Variable.objects.filter(raw__startswith="%s|%s|" % (code, name))[0]
            except AttributeError:
                continue
            except IndexError:
                name = "????"
                code = cell
                var = None
            name_set.add(name)
            print name, code, var.long_name if var else ""
        print "%d Unique Variables: %s" % (len(name_set), sorted(name_set))


def import_mvl(fh):
    """
    Takes a filehandle and extracts the variable within.
    """
    counter = 0
    n_created = 0
    for row in fh:
        variable, created = Variable.objects.get_or_create_from_mvl(row)
        counter += 1
        n_created += created
    return counter, n_created
