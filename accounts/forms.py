from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import get_user_model
from accounts.models import User
class UserCreateForm(UserCreationForm):
    class Meta():
        fields = ['username','email','password1','password2']
        model = User

    def __init__(self,*args,**kwargs):
        super(UserCreationForm,self).__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email address'
