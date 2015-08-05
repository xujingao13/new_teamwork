"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user_reg/$','player.views.user_reg'),
    url(r'^login/$','player.views.user_login'),
    url(r'^logout/(.*)$','player.views.user_logout'),
    url(r'to_user_reg/$','player.views.to_user_reg'),
    url(r'^$','player.views.user_login'),
    url(r'update/$','player.views.update'),
    url(r'update_password/(.*)$','player.views.update_password'),
    url(r'^to_update_password/(.*)$','player.views.to_update_password'),
    url(r'^gamehall/$', 'player.views.gamehall'),
    url(r'^player1/$', 'player.views.player1'),
    url(r'^player2/$', 'player.views.player2'),
    url('message/(.*)$', 'player.views.message'),
    url(r'^info/(.*)$','player.views.info'),
    url(r'^to_index/(.*)$','player.views.to_index'),
    url(r'^add_friend/(.*)$','player.views.add_friend'),
    url(r'^delete_friend/(\d*)a(\d*)$','player.views.delete_friend'),
    url(r'^check_friend_info/(.*)$','player.views.check_friend_info'),
    url(r'room(\d*)a(\d*)$', 'player.views.enterroom'),
]
