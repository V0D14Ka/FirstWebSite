from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Почта адресата',
                                                                     'style': 'width: 250px;',
                                                                     'class': 'form-control'}), required=True)
    subject = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Тема',
                                                                      'style': 'width: 250px;',
                                                                      'class': 'form-control'}), required=True)
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Сообщение',
                                                                     'style': 'width: 250px; height: 150px;',
                                                                     'class': 'form-control'}), required=True)


class WeatherForm(forms.Form):
    place = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Город',
                                                                    'style': 'width: 250px;',
                                                                    'class': 'form-control'}), required=True)


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
