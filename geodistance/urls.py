from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geodistance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.indexView, name='index'),
	url(r'^calculate/', views.calculate, name='calculate')
)
