from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members'
    def ready(self):
        from members.signals import create_group_permission
        post_migrate.connect(create_group_permission)