from __future__ import absolute_import

import csv
import logging
import os
import re
from collections import defaultdict

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
        years = defaultdict(list)
        for idx, cell in enumerate(header[2:]):
            if not cell:
                continue
            print idx, cell
            name, year = re.match(r'([A-Z0-9]+)\s\((\w+)\)', cell).groups()
            years[year].append((idx, name))
        self.years_data = years

    def parse_rows(self, institution_model, report_model):
        """
        Do stuff.
        """
        report_name = report_model.__name__
        for row in self._reader:
            if len("".join(row[2:])) == 0:
                # skip empty rows
                continue
            inst = institution_model.objects.get(ipeds_id=row[self.primary_idx])
            for year in self.years_data:
                new_data = dict()
                for idx, name in self.years_data[year]:
                    if row[idx]:
                        new_data[name] = row[idx]
                if new_data:
                    instance, created = report_model.objects.get_or_create(
                        institution=inst, year=year,
                        defaults=dict(year_type=self.year_type))
                    instance.__dict__.update(new_data)
                    instance.save()
                else:
                    # skip empty data
                    continue
                # TODO only log changed data
                # TODO make ints ints, decimals strings, floats float
                # camelCase for better JSON compatibility
                log_data = dict(firstImport=created,  # `created` is reserved
                                instPk=inst.pk, instName=inst.name, year=year,
                                report=report_name, newData=new_data,
                                source="ipeds")
                logger.info("%s" % (instance), extra=dict(json=log_data))

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
