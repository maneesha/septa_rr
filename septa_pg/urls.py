from django.conf.urls import patterns, include, url
from septa_pg import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'septa_pg.views.home', name='home'),
    # url(r'^septa_pg/', include('septa_pg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^search-form/$', views.search_form), 
    url(r'^search/$', views.search),
)
