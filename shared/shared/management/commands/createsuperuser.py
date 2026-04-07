from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

class Command(createsuperuser.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        email = options.get('email')
        if not email:
            raise CommandError('The --email argument is required.')
        super().handle(*args, **options)