from celery import Celery
from ms_fa.config import settings


redis_config = settings.redis_config
redis_host = redis_config.get("HOST")
redis_port = redis_config.get("PORT")
redis_db = redis_config.get("DATABASE")
redis_user = redis_config.get("USERNAME")
redis_pass = redis_config.get("PASSWORD")

auth = f'{redis_user}:{redis_pass}' if redis_pass else redis_user

celery = Celery('worker')
celery.conf.broker_url = f'redis://{auth}@{redis_host}:{redis_port}/1'
celery.conf.result_backend = f'redis://{auth}@{redis_host}:{redis_port}/2'
celery.conf.imports = ['ms_fa.tasks', 'ms_fa.tasks.update_cache']

