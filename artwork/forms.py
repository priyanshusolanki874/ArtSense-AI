from django import forms
from .models import Artwork, Contact
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ArtworkForm(forms.ModelForm):

    class Meta:
        model = Artwork
        fields = ['title', 'image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']