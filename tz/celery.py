import os
import celery
from tz import settings

app_test = celery.Celery('tz')
app_test.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
app_test.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
