## 数据库配置
import pymysql
pymysql.install_as_MySQLdb()

# celery 配置
from .celery import app as celery_app
__all__ = ['celery_app']