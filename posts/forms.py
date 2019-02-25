from django import forms

from posts import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "group")
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PostForm,self).__init__(*args, **kwargs)
        if user is not None:
            self.fields["group"].queryset = models.Group.objects.filter(members = user)