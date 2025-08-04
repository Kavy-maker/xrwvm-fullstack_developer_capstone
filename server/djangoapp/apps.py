from django.apps import AppConfig


class DjangoappConfig(AppConfig):
    name = 'djangoapp'

    def ready(self):
        import djangoapp.signals