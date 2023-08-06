from django.apps import AppConfig


class DuplicateConfig(AppConfig):
    name = 'duplicate'

    def ready(self):
        super().ready()
        import duplicate.checks  # noqa
