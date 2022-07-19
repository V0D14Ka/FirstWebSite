from django.core.mail import send_mail

from MySite.settings import EMAIL_HOST_USER
from main.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import UserPost
from main.tasks import send_spam


@receiver(post_save, sender=UserPost)
def make_spam(sender, instance, **kwargs):
    owner = instance.user_id
    send_spam.delay(owner)
