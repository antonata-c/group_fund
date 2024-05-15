from django.apps import AppConfig


class FundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fund'
    verbose_name = "Групповые денежные сборы"

    def ready(self):
        import fund.signals
