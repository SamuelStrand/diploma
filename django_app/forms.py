from django import forms
from django_app import models


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'description', 'price', 'image')

