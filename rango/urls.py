__author__ = 'Russell'

from django.conf.urls import patterns, url
from rango import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>\w+)$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    # url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^chords/$', views.chords, name='chords'),
    url(r'^favorites/$', views.favorites, name='favorites'),
    url(r'^add_favorite/$', views.add_favorite, name='add_favorite'),
    url(r'^del_favorite/$', views.del_favorite, name='del_favorite'),

    )