from django.test import TestCase

from ..models import VariableManager, Variable


class VariableManagerTest(TestCase):
    def test_get_or_create_from_mvl_strips_year(self):
        # assert we're testing VariableManager
        self.assertIsInstance(Variable.objects, VariableManager)

        row = 'FOO2000|FOO|Foo|Fooey||||||||||||||||||||||||'
        variable, created = Variable.objects.get_or_create_from_mvl(row)
        self.assertTrue(created)
        self.assertEqual(variable.code, 'FOO')  # strips year
        self.assertEqual(variable.short_name, 'FOO')
        self.assertEqual(variable.category, 'Foo')
        self.assertEqual(variable.long_name, 'Fooey')
        self.assertEqual(variable.year, '2000')

    def test_get_or_create_from_mvl_strips_DRV(self):
        # assert we're testing VariableManager
        self.assertIsInstance(Variable.objects, VariableManager)

        row = 'DRVFOO2000|FOO|Foo|Fooey||||||||||||||||||||||||'
        variable, created = Variable.objects.get_or_create_from_mvl(row)
        self.assertTrue(created)
        self.assertEqual(variable.code, 'FOO')  # strips year and DRV
        self.assertEqual(variable.short_name, 'FOO')
        self.assertEqual(variable.category, 'Foo')
        self.assertEqual(variable.long_name, 'Fooey')
        self.assertEqual(variable.year, '2000')

    def test_get_or_create_from_mvl_strips_DRV_and_suffix(self):
        # assert we're testing VariableManager
        self.assertIsInstance(Variable.objects, VariableManager)

        row = 'DRVFOO2000_RV|FOO|Foo|Fooey||||||||||||||||||||||||'
        variable, created = Variable.objects.get_or_create_from_mvl(row)
        self.assertTrue(created)
        self.assertEqual(variable.code, 'FOO')  # strips it alllll
        self.assertEqual(variable.short_name, 'FOO')
        self.assertEqual(variable.category, 'Foo')
        self.assertEqual(variable.long_name, 'Fooey')
        self.assertEqual(variable.year, '2000')

    def test_get_or_create_from_mvl_strips_handles_weird_years(self):
        # assert we're testing VariableManager
        self.assertIsInstance(Variable.objects, VariableManager)

        row = 'FOO0203|FOO|Foo|Fooey||||||||||||||||||||||||'
        variable, created = Variable.objects.get_or_create_from_mvl(row)
        self.assertEqual(variable.year, '2002')

        row = 'FOO1011|FOO|Foo|Fooey||||||||||||||||||||||||'
        variable, created = Variable.objects.get_or_create_from_mvl(row)
        self.assertEqual(variable.year, '2010')
