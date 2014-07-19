from django.db import models


class Variable(models.Model):
    """ An IPEDS report variable """
    code = models.CharField(max_length=20)
    short_name = models.CharField(max_length=8)
    category = models.CharField(max_length=150)
    long_name = models.CharField(max_length=80)
    raw = models.CharField(max_length=800, unique=True)
    used = models.BooleanField(default=False)


class Importer(models.Model):
    """
    A shim model just to get an entry and a form into the Django admin.
    """
    mvl_file = models.FileField('MVL file', upload_to='devnull/')
    imported_at = models.DateTimeField(auto_now_add=True)
    variables_total = models.PositiveSmallIntegerField(null=True, blank=True)
    variables_new = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'variables'
        verbose_name_plural = 'Import MVL'  # HACK to label admin link
