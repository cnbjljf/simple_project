#!/usr/bin/env python
'''

'''
import os
import sys

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )


from django.conf.urls import url
from django.contrib import admin
from WebChat import  views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^msg_send',views.send_msg,name='send_msg'),
    url(r'^get_msg',views.get_msg,name='get_msg'),
    url(r'GetHistoryRecord$',views.Get_History_Record,name='GetHistoryRecord'),
    url(r'file_upload$',views.file_upload,name='file_upload'),
    url(r'file_upload_progress$',views.file_upload_progress,name='file_upload_progress'),
    url('delete_cache_key$',views.delete_cache_key,name='delete_cache_key'),
    url('get_group_numbers$',views.get_group_numbers,name='get_group_numbers'),

]