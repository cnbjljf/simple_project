#!/usr/bin/env python

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from Simple_BBS import views

urlpatterns = [
    url(r'^$',views.category),
    url(r'^category/(\d+)/', views.category,name='category'),
    url(r'^detail_article/(\d+)$',views.article_detail,name='article_detail'),
    url(r'^comment/$',views.handler_comemnt,name='post_comment'),
    url(r'^comment_list/(\d+)/$',views.get_comments,name='get_comments'),
    url(r'^search_article$',views.search_article,name='search_article'),
    url(r'^add_article$',views.add_article,name='add_article'),
    url(r'^articles/(\d+)',views.article_modify)
]