from django.contrib import admin

from .models import Variable, Importer
from .utils import import_mvl


class VariableAdmin(admin.ModelAdmin):
    list_display = ('long_name', 'year', 'code', 'short_name', 'category',
        'is_derived', 'is_revised', 'favorite', )
    list_filter = ('code', 'short_name', 'year', 'favorite')
    list_per_page = 250  # limit of 250 variables per report
    readonly_fields = ('code', 'short_name', 'category', 'long_name', 'raw', 'year')
    search_fields = ('category', 'long_name')

    def is_derived(self, obj):
        return obj.is_derived
    is_derived.boolean = True

    def is_revised(self, obj):
        return obj.is_revised
    is_revised.boolean = True

    def make_MVL(self, request, queryset):
        from django.http import HttpResponse
        from datetime import datetime
        response = HttpResponse("".join(queryset.values_list('raw', flat=True)),
            mimetype="text/plain")
        filename = datetime.now().isoformat().split('.')[0].replace(':', '-')
        filename += "-q%s" % queryset.count()
        response['Content-Disposition'] = 'attachment; filename=ipeds-%s.mvl' % filename
        return response

    def mark_favorite(self, request, queryset):
        queryset.update(favorite=True)

    def unmark_favorite(self, request, queryset):
        queryset.update(favorite=False)
    actions = ['make_MVL', 'mark_favorite', 'unmark_favorite']
admin.site.register(Variable, VariableAdmin)


class ImporterAdmin(admin.ModelAdmin):
    readonly_fields = ('variables_total', 'variables_new')

    def save_model(self, request, obj, form, change):
        """HACK to keep admin from actually saving anything."""
        total, n_created = import_mvl(form.files['mvl_file'])
        obj.variables_total = total
        obj.variables_new = n_created
        obj.save()
admin.site.register(Importer, ImporterAdmin)
