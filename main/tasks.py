from MySite.celery import app
from django.core.mail import send_mail
from main.models import User
from MySite.settings import EMAIL_HOST_USER


@app.task
def send_spam(owner, title):
    subs = User.objects.get(id=owner).friends.all()
    name = User.objects.get(id=owner).username
    mesg = 'Здравствуйте. У пользователя ' + name + ' новый пост - ' \
           + '"' + title + '"' + '. С уважением, администрация проекта!'
    for i in subs:
        uuser = User.objects.get(id=i.user_id).email
        send_mail('Новое видео', mesg, EMAIL_HOST_USER, [uuser])

