from django.db import models
from Simple_BBS.models import UserProfile

# Create your models here.

class WebGroup(models.Model):
    name = models.CharField(max_length=64)
    brief = models.CharField(max_length=255,blank=True,null=True)
    owner = models.ForeignKey(UserProfile)
    admins = models.ManyToManyField(UserProfile,blank=True,related_name='group_admins')
    members = models.ManyToManyField(UserProfile,blank=True,related_name='group_members')
    max_members = models.IntegerField(default=200)

    def __str__(self):
        return self.name



class ChatRecord(models.Model):
    myself = models.ForeignKey(UserProfile)
    peer_self = models.ForeignKey(UserProfile,related_name='chat_peer')
    choice_type = (('single',u'单人'),
                   ('group',u'群组'))
    chat_type = models.CharField(choices=choice_type,max_length=20)
    TimeStamp = models.CharField(max_length=200)
    Content = models.CharField(max_length=100000)




