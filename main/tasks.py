from MySite.celery import app
from django.core.mail import send_mail
from main.models import User
from MySite.settings import EMAIL_HOST_USER


@app.task
def send_spam(owner):
    try:
        subs = User.objects.get(id=owner).friends.all()
        send_mail('mesg', subs, EMAIL_HOST_USER, ['minecraft35510880@gmail.com'])
    except:

        mesg = 'Здравствуйте'
    send_mail('mesg', 'popusk', EMAIL_HOST_USER, ['minecraft35510880@gmail.com'])
