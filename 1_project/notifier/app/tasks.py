from celery import Celery
import structlog
from config import config
from generator import (
    EmailGenerator,
    PushGenerator,
    SMSGenerator,
)
from constant import NotificationType

logger = structlog.get_logger(__name__)

app = Celery(
    'tasks',
    backend=config.redis_url,
    broker=config.broker_url
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
