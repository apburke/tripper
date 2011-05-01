from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tripper.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^(\d{4})$', 'year', name='year'),
    url(r'^(\d{4})/(\d{2})$', 'month_view', name='month'),
    # url(r'^(\d{4})/(\d{2})/w(\d{2})$', 'week', name='week'),
    # url(r'^(\d{4})/(\d{2})/d(\d{2})$', 'day', name='day'),

    # url(r'^tripper/', include('tripper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
