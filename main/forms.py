from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(label='Тема', required=True)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea, required=True)

