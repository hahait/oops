from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    """Run a development thrift server"""

    def handle(self, *args, **kwargs):
        print("我运行了")
