from django import forms
from django.forms import ModelForm, TextInput, FileInput, Form
from .models import Profile, Album, Photo


class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'image']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'last name'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'you@email.com'}),
        }


class ContactForm(Form):
    first_name = forms.CharField(max_length=255, label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=255, label='Subject', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    message = forms.CharField(max_length=255, label='Message', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Write your message or question here...', 'cols': 30, 'rows': 7}))


class AddAlbumForm(Form):
    album = forms.CharField(max_length=255, label='Album', widget=forms.TextInput(
        attrs={'class': 'form-control ', 'placeholder': 'Enter album name'}))


class AddPhotoForm(Form):
    image = forms.ImageField()


