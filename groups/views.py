# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,RedirectView)
from groups.models import *
from django.contrib import messages

class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request,*args,**kwargs):
        group = get_object_or_404(Group,slug = self.kwargs.get('slug'))
        user = get_object_or_404(User,username__iexact=self.request.user.username)
        try:
            group.members.add(user)
        except IntegrityError:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request,'You are now a member!')

        return super(JoinGroup,self).get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request,*args,**kwargs):
        user = get_object_or_404(User,username__iexact=self.request.user.username)

        group = get_object_or_404(Group,slug = self.kwargs.get('slug'))

        user.group.remove(group)

        messages.success(self.request,'You have left the group!')

        return super(LeaveGroup,self).get(request,*args,**kwargs)
