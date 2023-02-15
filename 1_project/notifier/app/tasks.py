from celery import Celery
import structlog
from config import config

logger = structlog.get_logger(__name__)

app = Celery(
    'tasks',
    backend=config.redis_url,
    broker=config.broker_url
)


def get_generator(notification_type):
    if notification_type == 'push':
        return ...


@app.task(queue='high_priority')
def queue_high_priority_notification(message, user_id, notification_type):
    generator = get_generator(notification_type)
    notification = generator.make_notification(
        message, user_id
    )
    notification.send()


@app.task(queue='default')
def queue_notification(message, user_id, notification_type):
    generator = get_generator(notification_type)
    notification = generator.make_notification(
        message, user_id
    )
    notification.send()
