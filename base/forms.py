from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Lesson, UserProfile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'name', 'about']
        labels = {
            'avatar': ('Zdjęcie profilowe'),
            'name': ('Nazwa użytkownika'),
            'about': ('Kilka słów o mnie'),
        }

        widgets = {
            'avatar': forms.FileInput(),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': ('login'),
            'email': ('email'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'hasło'
        self.fields['password2'].label = 'powtórz hasło'

        self.fields['username'].widget.attrs['placeholder'] = 'Podaj login'
        self.fields['email'].widget.attrs['placeholder'] = 'Podaj email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Podaj hasło'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_name', 'video']
        labels = {
            'lesson_name': ('Nazwa lekcji'),
            'video': ('Film do lekcji'),
        }
