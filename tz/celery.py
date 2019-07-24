import os
import celery
app_test = celery.Celery('tz')
app_test.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
