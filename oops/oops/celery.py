from __future__ import absolute_import
import os
import django
from celery import Celery, platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oops.settings')
django.setup()
app = Celery('oops')
# 默认情况下，celery 是不建议 以 root 用户启动的，使用下面这个配置，就可以规避这个限制
platforms.C_FORCE_ROOT = True
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)