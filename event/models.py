from django import forms
from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    class Meta:
        verbose_name = 'Мероприятия'
        verbose_name_plural = 'Мероприятие'
    name = models.CharField(max_length=100)
    author = models.ForeignKey('auth.User')
    image = models.ImageField(upload_to="event")
    address = models.TextField()
    description = models.TextField()
    elect = models.BooleanField(default=0)

    def event_get(self, user):
        return Event_User.objects.filter(event=self, user=user).exists()

    def __str__(self):
        return self.name


class Event_User(models.Model):
    class Meta:
        verbose_name = 'Чекины'
        verbose_name_plural = 'Чекин'
    user = models.ForeignKey('auth.User')
    event = models.ForeignKey('Event')

    def __str__(self):
        return '{0} {1}'.format(self.event, self.user)


class RegisterForm(forms.Form):
    login = forms.CharField(label='Логин', min_length=5)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль 2', min_length=8, widget=forms.PasswordInput)
    email = forms.CharField(label='E-mail', min_length=1)
    last_name = forms.CharField(label='Фамилия', min_length=1)
    first_name = forms.CharField(label='Имя', min_length=1)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Пароли не совпадают")
        usrs = User.objects.filter(username=cleaned_data.get('login'))
        if len(usrs) > 0:
            raise forms.ValidationError("Логин занят")


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин', min_length=5)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)


class EventForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.author = user

    class Meta:
        model = Event
        fields = ['name', 'image', 'address', 'description']
        labels = {
            "name": "Название",
            'image': "Картинка",
            'address': "Адрес",
            'description': "Описание",
        }
