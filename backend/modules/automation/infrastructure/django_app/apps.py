import os
import threading
from django.apps import AppConfig
from django.conf import settings


class AutomationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.automation.infrastructure.django_app'
    label = 'automation'

    _worker_started = False

    def ready(self):
        # Arrancar worker en segundo plano solo si está habilitado por env y evitar doble inicio por el autoreloader
        if not getattr(settings, 'START_AUTOMATION_WORKER', False):
            return
        if os.environ.get('RUN_MAIN') != 'true':
            return
        if AutomationConfig._worker_started:
            return

        from modules.automation.infrastructure.worker import run_worker

        t = threading.Thread(target=run_worker, name='automation-worker', daemon=True)
        t.start()
        AutomationConfig._worker_started = True


