from django.core.management import BaseCommand

from permission.permissions import update_permissions


class Command(BaseCommand):
    """
    Update permissions
    """

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Updating permissions..."))
        permissions = update_permissions()
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated permissions. Created {permissions} permissions."
            )
        )
