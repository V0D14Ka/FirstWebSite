from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': 'Почта адресата',
                                                                                    'style': 'width: 250px;',
                                                                                    'class': 'form-control'}),
                             required=True)
    subject = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': 'Тема',
                                                                                     'style': 'width: 250px;',
                                                                                     'class': 'form-control'}),
                              required=True)
    message = forms.CharField(max_length=300, label='', widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                                                                     'style': 'width: 250px; height: 150px;',
                                                                                     'class': 'form-control'}),
                              required=True)


class WeatherForm(forms.Form):
    place = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'placeholder': 'Город',
                                                                                   'style': 'width: 250px;',
                                                                                   'class': 'form-control'}),
                            required=True)


class HoroscopeForm(forms.Form):
    sign_choices = (("oven", "Овен"),
                    ("telets", "Телец"),
                    ("bliznetsi", "Близнецы"),
                    ("rac", "Рак"),
                    ("lev", "Лев"),
                    ("deva", "Дева"),
                    ("vesy", "Весы"),
                    ("scorpion", "Скорпион"),
                    ("strelets", "Стрелец"),
                    ("kozerog", "Козерог"),
                    ("vodoley", "Водолей"),
                    ("riby", "Рыбы"),
                    )
    sign = forms.ChoiceField(label="Знак зодиака", choices=sign_choices)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=12, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(max_length=40, label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(max_length=30, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(max_length=30, label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует!")
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=12, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=30, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
