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

