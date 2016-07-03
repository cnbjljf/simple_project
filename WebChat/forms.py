#!/usr/bin/env python
'''

'''
import os
import sys

from django.forms import Form,ModelForm
from WebChat import forms
from WebChat import models

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

def get_form(class_name,*args,**kwargs):
    '''
    装饰器，用来处理form表单用的
    :param class_name: models里面的哪个表名
    :param args:  列表形式的参数
    :param kwargs:   字典形式的参数
    :return:
    '''
    class modeform(forms.ModelForm):
        class Meta:
            model = class_name
            exclude = ()

        def __init__(self,*args,**kwargs):
            super(modeform,self).__init__(*args,**kwargs)
            for field_name in self.base_fields:
                field = self.base_fields[field_name]
                field.widget.attrs.update({'class':'form-control'})

    return modeform(*args,**kwargs)