from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'description']

class NewUserForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone',]