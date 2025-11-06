from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import CustomUser


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="전화번호", max_length=20, required=False)
    address = forms.CharField(label="주소", max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email", "phone")

