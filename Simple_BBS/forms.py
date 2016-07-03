from Simple_BBS import models
from django.forms import Form,ModelForm
from django import forms
from django.core.exceptions import ValidationError


def get_form(classname,*args,**kwargs):
    # def __init__(self):
    #     super(ModelForm, self).__init__(*args, **kwargs)
    #     print("aaa")
    class ModelForm(forms.ModelForm):
        class Meta:
            model = classname
            exclude = ('author','pub_date','priority')
        def __init__(self,*args,**kwargs):
            super(ModelForm,self).__init__(*args,**kwargs)
            for field_name in self.base_fields:
                field = self.base_fields[field_name]
                field.widget.attrs.update({'class':'form-control'})
    return ModelForm(*args,**kwargs)



class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        exclude = ()

    def __init__(self,*args,**kwargs):
        super(CommentForm,self).__init__(*args,**kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})