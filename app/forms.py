from django import forms

from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from app.models import Customer
from app.models import CustomUser

# from .models import Customer

class LoginForm(AuthenticationForm):
    #  username=forms.CharField(label='Name',widget=forms.TextInput
    #                          (attrs={'autofocus':"True",'placeholder':'username','class':"form-control"}))
    email=forms.EmailField(label='Email',widget=forms.EmailInput
                          (attrs={'class':'form-control'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput
                             (attrs={'placeholder':'password','autocomplete':'current-password','class':'form-control'}))

class RegistrationForm(UserCreationForm):
    # username=forms.CharField(widget=forms.TextInput
    #                          (attrs={'autofocus':"True",'class':"form-control"}))
    email=forms.EmailField(label='Email',widget=forms.EmailInput
                          (attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput
                             (attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput
                             (attrs={'class':'form-control'}))
    class Meta:
        model=CustomUser
        fields=['email','password1','password2']

     

class ResetPassword(PasswordChangeForm):
    pass
 

class ProfileForm(forms.ModelForm):

    class Meta:

        model=Customer

        fields=['name','locality','city','mobile','state','zipcode']

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'})
        }
        
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget = forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget = forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))    
    new_password2 = forms.CharField(label='Confirm Password',widget = forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))