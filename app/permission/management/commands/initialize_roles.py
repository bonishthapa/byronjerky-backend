from django.core.management import BaseCommand

from permission.models import Role, UserRole


class Command(BaseCommand):
    """
    Update permissions
    """

    def handle(self, *args, **options):
        roles = [UserRole.ADMIN.value]
        for role in roles:
            _, created = Role.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Role {role}"))
            else:
                self.stdout.write(self.style.NOTICE(f"Role {role} already exists"))
