from django import forms
from django.contrib.auth.models import User
from news.models import Account, Link

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['karma', 'user']

class LinkForm(forms.ModelForm):
    #url = forms.URLField(max_length=200, help_text="Please enter the URL of the link.")
    #title = forms.CharField(max_length=128, help_text="Please enter the title")
    url = forms.URLField(max_length=200)
    title = forms.CharField(max_length=128)

    class Meta:
        model = Link

        fields = ['url', 'title']

class EmailForm(forms.Form):
    email = forms.EmailField()
