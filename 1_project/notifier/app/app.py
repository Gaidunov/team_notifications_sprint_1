import structlog
from flask import Flask, request
from .tasks import queue_high_priority_notification, queue_notification

logger = structlog.get_logger(__name__)

app = Flask(__name__)


@app.route('api/queue_notificaton', methods=['POST'])
def queue_notification():
    message_type = request.json['type']
    message = request.json['message']
    user_id = request.json['user_id']

    if message_type == 'priority':
        queue_high_priority_notification.delay(
            message, user_id
        )
        return

    queue_notification.delay(
        message, user_id
    )


if __name__ == '__main__':
    app.run(debug=True)
