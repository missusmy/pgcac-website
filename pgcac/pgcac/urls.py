from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Static pages
    url(r'^$', 'pgcac.views.index', name='index'),
    url(r'^about/privacypolicy$', 'pgcac.views.privacypolicy', name='privacypolicy'),
    url(r'^about/website$', 'pgcac.views.website', name='website'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # This should not happen in production - serve by apache!
    url(r'^media/(.*)$', 'django.views.static.serve', {
        'document_root': '../media',
    }),
    url(r'^(favicon.ico)$', 'django.views.static.serve', {
        'document_root': '../media',
    }),
)
