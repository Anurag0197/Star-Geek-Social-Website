# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from groups.models import Group
from accounts.models import User

from django import template
register = template.Library()
# Create your models here.

class Post(models.Model):
    message = models.TextField()
    created_at = models.DateField(auto_now = True)
    user = models.ForeignKey(User,related_name='posts',on_delete = models.CASCADE)
    group = models.ForeignKey(Group,related_name='posts',on_delete = models.CASCADE)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('posts:single',kwargs = {'username':self.user.username,'pk':self.pk})

    class Meta():
        ordering = ['-created_at']
