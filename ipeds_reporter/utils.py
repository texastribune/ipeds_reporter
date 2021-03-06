from collections import defaultdict, namedtuple
import csv
import re


class IpedsCSVReader(object):
    """
    A special CSV reader for IPEDS reports.
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
        IPEDSCell = namedtuple('IPEDSCell', 'short_name, year, raw_code')
        # the first two columns are the institution id and name
        for idx, cell in enumerate(header):
            if idx < 2:
                header_parsed[idx] = cell
                continue
            # DELETEME this is just a hack to get around the last empty col
            if not cell:
                continue
            short_name, raw_code = re.match(r'(\w+)\s\((\w+)\)', cell).groups()
            # XXX begin copy pasted from ipeds_reporter/models.py
            butts = re.match(r'(DRV)?([a-zA-Z]+)(\d{4})', raw_code).groups()
            __, code, year = butts
            if int(year[:2]) == int(year[2:]) - 1:
                # I've only found post Y2K years this has happened
                year = u'20' + year[:2]
            # XXX end
            header_parsed[idx] = IPEDSCell(short_name, year, raw_code)
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
        cells = [x for x in self.header_parsed if isinstance(x, tuple)]
        short_names = [x.short_name for x in cells]
        unique_short_name = list(set(short_names))
        years = defaultdict(list)
        for cell in cells:
            years[cell.short_name].append(cell.year)
        return {
            'columns': len(cells),  # shape
            'unique short_names': unique_short_name,
            'years': years,
        }


def import_mvl(fh):
    """
    Takes a filehandle and extracts the variable within.
    """
    from .models import Variable  # avoid django import at the root

    counter = 0
    n_created = 0
    for row in fh:
        variable, created = Variable.objects.get_or_create_from_mvl(row)
        counter += 1
        n_created += created
    return counter, n_created
