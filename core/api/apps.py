from django.apps import AppConfig


class ApiConfig(AppConfig):
	default_auto_field = "django.db.models.BigAutoField"
	name = "api"

	# load the signals when the app is initialized
	def ready(self):
		from . import signals