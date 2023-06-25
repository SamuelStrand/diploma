from django import forms
from django_app import models


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'description', 'price', 'image')


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('user', 'profile_image', 'first_name', 'last_name', 'email', 'phone_number')
