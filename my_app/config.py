from datetime import timedelta

SQLALCHEMY_DATABASE_URI  = 'sqlite:////home/pi/flask_env/my_app/home_automation/home_automation.db'

CELERY_BROKER_URL = 'amqp://localhost//'
CELERY_RESULT_BACKEND = 'db+sqlite:////home/pi/flask_env/my_app/home_automation/home_automation.db'
CELERYBEAT_SCHEDULE = {
    'add-every-10-seconds': {
        'task': 'send_request',
        'schedule': timedelta(seconds=30)
    },
}


