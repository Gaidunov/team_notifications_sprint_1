from celery import Celery

celery = Celery(__name__, broker='amqp://localhost')

@celery.task
def add_to_queue(message, user_id, queue):
    if queue == 'priority':
        # Добавить сообщение в очередь priority
        print(f'Adding {message} to priority queue for user {user_id}')
    else:
        # Добавить сообщение в очередь plain
        print(f'Adding {message} to plain queue for user {user_id}')
