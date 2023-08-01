from django import forms
from .models import CustomUser, Listings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import EmailValidator


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, label="Nazwa użytkowanika")
    password = forms.CharField(max_length=30, required=True, label="Hasło", widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label="Nazwa użytkownika")
    first_name = forms.CharField(max_length=30, required=True, label="Imię")
    last_name = forms.CharField(max_length=30, required=True, label="Nazwisko")
    email = forms.EmailField(max_length=254, required=True, label="E-mail", validators=[EmailValidator])
    password1 = forms.CharField(max_length=30, required=True, label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, required=True, label="Powtórz Hasło", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UpdateUserDetailsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'avatar', 'bio']


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['image_1', 'image_2', 'image_3', 'title', 'description', 'category', 'artist', 'genre', 'condition',
                  'price']
