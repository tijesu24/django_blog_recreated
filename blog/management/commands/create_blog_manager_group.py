from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.apps import apps


class Command(BaseCommand):
    help = 'Create Blog Managers group with specific permissions'

    def handle(self, *args, **kwargs):
        # Create the group
        group, created = Group.objects.get_or_create(name='Blog Managers')

        # List of permissions to add to the group
        permissions = [
            'add_post',
            'change_post',
            'delete_post',
            'publish_post',
            'change_comment',
            'delete_comment'
        ]

        # Assign the permissions to the group
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created Blog Managers group and assigned permissions'))
