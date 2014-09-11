from StringIO import StringIO
import os

from django.test import TestCase

from ..utils import IpedsCSVReader, import_mvl


BASE_DIR = os.path.dirname(__file__)


class IpedsCSVReaderTest(TestCase):
    def test_it_works(self):
        with open(os.path.join(BASE_DIR, 'support', 'Data_7-20-2014.csv')) as fh:
            reader = IpedsCSVReader(fh)
            self.assertTrue(reader.header)
            self.assertTrue(reader.header_parsed)
            for row in reader:
                self.assertTrue(row)
            self.assertTrue(reader.explain_header())

    def test_parse_header_works(self):
        mock_csv = StringIO(
            'UnitID,Institution Name,CINDON (DRVIC2012),CINSON (DRVIC2012),'
            'chg2ay3 (IP1999AY),chg3ay3 (IP1999AY),'
        )
        reader = IpedsCSVReader(mock_csv)
        self.assertTrue(reader.header)
        self.assertTrue(reader.header_parsed)
        self.assertEqual(reader.header_parsed[0], 'UnitID')
        self.assertEqual(reader.header_parsed[1], 'Institution Name')
        cell = reader.header_parsed[2]
        self.assertEqual(cell.short_name, 'CINDON')
        self.assertEqual(cell.year, '2012')
        cell = reader.header_parsed[3]
        self.assertEqual(cell.short_name, 'CINSON')
        self.assertEqual(cell.year, '2012')
        cell = reader.header_parsed[4]
        self.assertEqual(cell.short_name, 'chg2ay3')
        self.assertEqual(cell.year, '1999')
        cell = reader.header_parsed[5]
        self.assertEqual(cell.short_name, 'chg3ay3')
        self.assertEqual(cell.year, '1999')


class ImportMVLTest(TestCase):
    """import_mvl"""
    def test_it_works(self):
        with open(os.path.join(BASE_DIR, 'support', 'DC_MasterFile_718631.mvl')) as fh:
            count, created = import_mvl(fh)
            self.assertEqual(count, created)
            self.assertEqual(count, 40)

        with open(os.path.join(BASE_DIR, 'support', 'DC_MasterFile_718631.mvl')) as fh:
            count, created = import_mvl(fh)
            self.assertEqual(count, 40)
            self.assertEqual(created, 0)
