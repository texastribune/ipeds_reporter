import os

from django.test import TestCase

from ..utils import IpedsCSVReader, import_mvl


BASE_DIR = os.path.dirname(__file__)


class IpedsCSVReaderTest(TestCase):
    def test_it_works(self):
        with open(os.path.join(BASE_DIR, 'support', 'Data_7-20-2014.csv')) as fh:
            reader = IpedsCSVReader(fh)
            print reader.header
            print reader.header_parsed


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
