from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.feed, name='feed'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^test/$', views.test, name='test'),
    url(r'^add_link/$', views.add_link, name='add_link'),
    url(r'^up_link/$', views.up_link, name='up_link'),
    url(r'^about/$', views.about, name='about'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^latest/$', views.latest_news, name='latest'),
    url(r'^account/$', views.account, name='account'),
    url(r'^change_password/$', auth_views.password_change, {'template_name': 'news/change_password.html'}, name='change_password'),
    url(r'^password-change-done/$', auth_views.password_change_done,{'template_name': 'news/password_change_done.html'}, name='password_change_done'),
]
