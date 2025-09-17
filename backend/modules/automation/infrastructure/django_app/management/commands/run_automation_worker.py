from django.core.management.base import BaseCommand
from modules.automation.infrastructure.worker import run_worker


class Command(BaseCommand):
    help = 'Run automation worker (RabbitMQ consumer)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting automation worker...'))
        run_worker()

