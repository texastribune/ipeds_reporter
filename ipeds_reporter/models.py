import re

from django.db import models


class VariableManager(models.Manager):
    def get_or_create_from_mvl(self, raw):
        """Get or create from line in MVL."""
        bits = raw.split('|')
        code, short_name, category, long_name = bits[:4]
        code = re.match(r'(DRV)?([a-zA-Z]+)', code).groups()[1]
        data = dict(
            code=code,
            short_name=short_name,
            category=category,
            long_name=long_name,
        )
        return self.get_or_create(raw=raw, defaults=data)


class Variable(models.Model):
    """An IPEDS report variable."""
    code = models.CharField(max_length=20)
    short_name = models.CharField(max_length=8)
    category = models.CharField(max_length=150)
    long_name = models.CharField(max_length=80)
    raw = models.CharField(max_length=800, unique=True)
    used = models.BooleanField(default=False)

    # derived data
    year = models.CharField(max_length=4)  # TODO

    # MANAGERS #
    objects = VariableManager()

    def __unicode__(self):
        return u'{} ({})'.format(self.short_name, self.year)


class Importer(models.Model):
    """
    A shim model just to get an entry and a form into the Django admin.
    """
    mvl_file = models.FileField('MVL file', upload_to='devnull/')
    imported_at = models.DateTimeField(auto_now_add=True)
    variables_total = models.PositiveSmallIntegerField(null=True, blank=True)
    variables_new = models.PositiveSmallIntegerField(null=True, blank=True)
    # WISHLIST keep track of `User`

    class Meta:
        verbose_name = 'variables'  # HACK to label admin link
        verbose_name_plural = 'Import MVL'  # HACK to label admin link
