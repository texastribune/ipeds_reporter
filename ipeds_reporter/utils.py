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


class IpedsCsvReader(object):
    field_mapping = None
    primary_mapping = None
    year_type = None

    def __init__(self, fh, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._reader = self.get_reader(fh)
        self.parse_header()

    def get_reader(self, fh):
        return csv.reader(fh)

    def parse_header(self):
        header = self._reader.next()
        self.header = header
        if self.field_mapping is None:
            return
        years = defaultdict(list)
        fields = dict(self.field_mapping)
        primary_idx = None
        for idx, cell in enumerate(header):
            if cell == self.primary_mapping[0]:
                primary_idx = idx
                continue
            try:
                name, year = re.match(r'(\w+)\([a-zA-Z]+(\d+)', cell).groups()
            except AttributeError:
                continue
            if name in fields:
                years[year].append((idx, fields[name]))
        self.primary_idx = primary_idx
        self.years_data = years

    def parse_rows(self, institution_model, report_model):
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