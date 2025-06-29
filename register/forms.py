from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import re
from .models import Blog

class SignUp(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {
            'username': '',  # ← This removes the default message
        }
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if(len(password)<6):
            raise forms.ValidationError("Password must contain at least 6 characters long")
        if( not re.search(r'[0-9]',password)):
            raise forms.ValidationError("Password must contain at least one digit")
        if(not re.search(r'[A-Z]',password)):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        if(not re.search(r'[a-z]',password)):
            raise forms.ValidationError("Password must contain at least one lowercase letter")
        if(not re.search(r'[!@#$%^&*()_{},.|?:"<>]',password)):
            raise forms.ValidationError("Password must contain at least one special character")
        return password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class Login(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ['title','content']
