from django import forms
from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'author', 'image', 'address', 'description']
        labels = {
            "name": "Название",
            'author': "Автор",
            'image': "Картинка",
            'address': "Адрес",
            'description': "Описание",
        }
