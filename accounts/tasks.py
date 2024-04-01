from celery import shared_task

from accounts.models import User


@shared_task
def user_count():
    return User.objects.count()
