#coding:utf-8
__author__ = 'littlepig'
from django import forms

class CheckUserInfo(forms.Form):
    username = forms.CharField(label='账号', max_length=128, widget=forms.TextInput(attrs={'class': 'text-input'}))

class AddFriend(forms.Form):
    username = forms.CharField(label='账号', max_length=128, widget=forms.TextInput(attrs={'class': 'text-input'}))

class UpdateInfo(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'info_image-input'}))
    nickname = forms.CharField(label='昵称', max_length=128, widget=forms.TextInput(attrs={'class':'text-input'}))

class UpdatePasswordForm(forms.Form):
    origin_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pass_text-input'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pass_text-input'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pass_text-input'}))

    def validate(self,p1,p2):
        return p1==p2

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input'}))


class RegForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'reg_image-input'}))
    username = forms.CharField(label='账号', max_length=128,widget=forms.TextInput(attrs={'class':'text-input'}))
    nickname = forms.CharField(label='昵称', max_length=128,widget=forms.TextInput(attrs={'class':'text-input'}))
    password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class': 'text-input'}))
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput(attrs={'class': 'text-input'}))

    def validate(self,p1,p2):
        return p1==p2

    def clean_user_name(self):
        username = self.cleaned_data['username']
        length = len(username)
        if length < 4:
            raise forms.ValidationError("名字太短")
        return username
