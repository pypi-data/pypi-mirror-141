from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DjangoPowerAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_power_admin'
    verbose_name = _("Django Power Admin")
