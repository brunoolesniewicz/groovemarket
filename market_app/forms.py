from django import forms
from .models import CustomUser, Listings, Offers, Conversations, Messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.validators import EmailValidator


class LoginForm(AuthenticationForm):
    """
    LoginForm: Formularz logowania użytkownika z polem na nazwę użytkownika i hasło.
    """

    username = forms.CharField(max_length=30, required=True, label="Nazwa użytkowanika")
    password = forms.CharField(max_length=30, required=True, label="Hasło", widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': "Nieprawidłowa nazwa użytkownika lub hasło."
    }


class CreateUserForm(UserCreationForm):
    """
    CreateUserForm: Formularz rejestracji użytkownika z polami na nazwę użytkownika, imię, nazwisko, e-mail i hasło.
    """

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
    """
    UpdateUserDetailsForm: Formularz aktualizacji szczegółów użytkownika, w tym avataru, opisu i innych danych.
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'avatar', 'bio']


class CreateListingForm(forms.ModelForm):
    """
    CreateListingForm: Formularz tworzenia nowej oferty zawierający zdjęcia, tytuł, opis, kategorię, artystę, gatunek,
     stan i cenę.
    """

    class Meta:
        model = Listings
        fields = ['image_1', 'image_2', 'image_3', 'title', 'description', 'category', 'artist', 'genre', 'condition',
                  'price']


class CreateOfferForm(forms.ModelForm):
    """
    CreateOfferForm: Formularz tworzenia oferty na konkretną ofertę, zawierający cenę, użytkownika i ofertę.
    """

    class Meta:
        model = Offers
        fields = ['price', 'user', 'listing']
        widgets = {
            'user': forms.HiddenInput(),
            'listing': forms.HiddenInput()
        }


class CreateConversationForm(forms.ModelForm):
    """
    CreateConversationForm: Formularz tworzenia nowej rozmowy z opcjonalnie podanym użytkownikiem i ofertą.
    """

    class Meta:
        model = Conversations
        fields = ['sender', 'receiver', 'listing']
        widgets = {
            'sender': forms.HiddenInput(),
            'receiver': forms.HiddenInput(),
            'listing': forms.HiddenInput()
        }


class CreateMessageForm(forms.ModelForm):
    """
    CreateMessageForm: Formularz tworzenia nowej wiadomości w ramach rozmowy, zawierający tekst wiadomości.
    """

    class Meta:
        model = Messages
        fields = ['conversation', 'sender', 'body']
        widgets = {
            'conversation': forms.HiddenInput(),
            'sender': forms.HiddenInput(),
            'body': forms.Textarea(attrs={'rows': 2})
        }
        labels = {
            'body': 'Wiadomość'
        }


class ChangePasswordForm(PasswordChangeForm):
    """
    ChangePasswordForm: Formularz zmiany hasła użytkownika, z polami na stare i nowe hasło oraz jego potwierdzenie.
    """

    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Stare hasło'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Nowe hasło'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Potwierdź nowe hasło'
    )

    error_messages = {
        'password_mismatch': 'Nowe hasła nie są takie same.'
    }
