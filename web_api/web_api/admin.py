from django.contrib import admin
from django.apps import apps


# Register all the models we've created so they appear in Django Admin
for model in apps.get_app_config('web_api').models.values():
    admin.site.register(model)
