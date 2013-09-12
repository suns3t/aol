from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings as SETTINGS
from .views import home
from .views import lakes
from .views import maps

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home.home, name='home'),
    url(r'^about/?$', home.about, name='about'),
    url(r'^credits/?$', home.credits, name='credits'),
    url(r'^lakes/?$', lakes.listing, name='lakes-listing'),
    url(r'^lakes/(?P<reachcode>\d+)?$', lakes.detail, name='lakes-detail'),
    url(r'^map/?$', maps.home, name='map'),
    url(r'^map/lakes\.kml$', maps.lakes, name='lakes-kml'),
	url(r'^search/?$', lakes.search, name='lakes-search'),
    url(r'^photo-submissions/?$', home.photo_submissions, name='photo-submissions'),
    
    # Examples:
    # url(r'^$', 'aol.views.home', name='home'),
    # url(r'^aol/', include('aol.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(SETTINGS.MEDIA_URL, document_root=SETTINGS.MEDIA_ROOT)
