from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .forms import EmailForm
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'main/index.html')


def sendmail(request):
    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = "vodi4kaweb@mail.ru"
            try:
                send_mail(subject, message, from_email, [email])
            except BadHeaderError:
                return HttpResponse('Invalid Header found')
            return redirect('sent')
    return render(request, 'main/sendmail.html', {'form': form})


def sent(request):
    return render(request, 'main/sent.html')


def egg(request):
    return render(request, 'main/egg.html')
