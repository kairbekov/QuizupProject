from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainapp.views import home_view

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mainapp.views.home_view', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mainapp/', include('mainapp.urls')),
    #url(r'', include('gcm.urls')),
    #home page ENTalapp
    #url(r'^&', home_view),
)

admin.site.site_header = 'Admin site'
admin.site.site_title = 'ENT prepairing'
