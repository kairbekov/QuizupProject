from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'QuizupProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mainapp/', include('mainapp.urls')),
)

admin.site.site_header = 'Admin site'
admin.site.site_title = 'ENT prepairing'
