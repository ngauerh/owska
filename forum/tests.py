# from django.test import TestCase

# Create your tests here.
from django.conf import settings
import redis
r = redis.Redis(host=settings.REDIS_HOSTS, port=settings.REDIS_PORT, password=settings.REDIS_PASSWD, db=2)

r.lpush('niu', '123')