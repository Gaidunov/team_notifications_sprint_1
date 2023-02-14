from flask import Flask, request
from celery import Celery

app = Flask(__name__)
celery = Celery(__name__, broker='amqp://localhost')

@app.route('/add_to_queue_message', methods=['POST'])
def add_to_queue():
    message_type = request.json['type']
    message = request.json['message']
    user_id = request.json['user_id']
    queue = 'priority' if message_type == 'priority' else 'plain'
    task = celery.send_task('tasks.add_to_queue', args=[message, user_id, queue], queue=queue)
    return f'Task {task.id} added to {queue} queue'

if __name__ == '__main__':
    app.run(debug=True)
