# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import UserCreateForm
from accounts.models import User
# Create your views here.

class SignUp(CreateView):
    form_class = UserCreateForm
    model = User
    template_name = 'accounts/signup.html'
