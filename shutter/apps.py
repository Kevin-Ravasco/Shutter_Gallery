from django.apps import AppConfig


class ShutterConfig(AppConfig):
    name = 'shutter'

    def ready(self):
        import shutter.signals
