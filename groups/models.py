# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from django import template
register = template.Library()

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length = 255,unique = True)
    slug = models.SlugField(allow_unicode = True,unique = True)
    description = models.TextField(default = '')
    members = models.ManyToManyField(User,related_name = "group")

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Group,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs = {'slug':self.slug})

    def __str__(self):
        return self.name
