from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # the site IS the admin site
    url(r'', include(admin.site.urls)),
)
