from celery import Celery
import structlog
from .config import config
from generator import (
    EmailGenerator,
    PushGenerator,
    SMSGenerator,
)
from constant import NotificationType
from celery.schedules import crontab
from ..models import Notification
from datetime import datetime, timedelta, time
import pytz

logger = structlog.get_logger(__name__)

app = Celery(
    'tasks',
    backend=config.redis_url,
    broker=config.broker_url
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=1),
        queue_periodic_notifications.s(),
        expires=10
    )


class NotificationTypeDoesNotExistError(Exception):
    ...


def get_generator(notification_type):
    if notification_type == NotificationType.EMAIL:
        return EmailGenerator
    elif notification_type == NotificationType.PUSH:
        return PushGenerator
    elif notification_type == NotificationType.SMS:
        return SMSGenerator
    else:
        raise NotificationTypeDoesNotExistError


@app.task(queue='high_priority')
def queue_high_priority_notification(
    message: str,
    user_id: int,
    notification_type: str
) -> None:
    user_data = {'name': 'client_name'}  # api reqeust here

    generator = get_generator(notification_type)
    notification = generator(
        message, user_data.get('name')
    ).make_notification()
    notification.send()


@app.task(queue='default')
def queue_notification(
    message: str,
    user_id: int,
    notification_type: str
) -> None:
    user_data = {'name': 'client_name'}  # api reqeust here

    generator = get_generator(notification_type)
    notification = generator(
        message, user_data.get('name')
    ).make_notification()
    notification.send()


@app.task(queue='default')
def queue_periodic_notifications() -> None:
    notifications = Notification.objects.filter(
        send_at__lte=datetime.now() + timedelta(days=1),
    )

    updated_notifications = []

    for notif in notifications:
        client_time = datetime.now(pytz.timezone(notif.timezone))

        if time(hour=8) <= client_time.time() <= time(hour=18):
            user_data = {'name': 'client_name'}  # api reqeust here

            notification = EmailGenerator(
                'Have you seen our new films? Click the link to see them!', user_data.get('name')
            ).make_notification()

            notification.send()

            notif.send_at = datetime.utcnow()
            updated_notifications.append(notif)

        Notification.objects.bulk_update(
            updated_notifications,
            fields=('send_at',)
        )
