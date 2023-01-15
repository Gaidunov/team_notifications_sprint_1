from .app import celery as app


@app.task
def my_background_task():
    print('bebra')
