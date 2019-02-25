# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic
from django.shortcuts import get_object_or_404

from braces.views import SelectRelatedMixin

from . import forms
from . import models

from accounts.models import User

# Create your views here.

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            self.username = get_object_or_404(User,username__iexact=self.kwargs.get("username"))
            return models.Post.objects.filter(user=self.username)
        else:
            raise Http404

class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super(PostDetail,self).get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get("username"))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    form_class = forms.PostForm
    model = models.Post

    def get_form_kwargs(self):
         kwargs = super(CreatePost,self).get_form_kwargs()
         kwargs.update({"user": self.request.user})
         return kwargs

    def form_valid(self,form):
        self.object = form.save(commit = False)
        user = get_object_or_404(User,username__iexact=self.request.user.username)
        self.object.user = user
        self.object.save()
        return super(CreatePost,self).form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super(DeletePost,self).delete(*args, **kwargs)
