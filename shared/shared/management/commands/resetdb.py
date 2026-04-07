from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = '💣 Resets the database: flushes, makes migrations, migrates, optionally creates superuser.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Run without interactive prompts (for automation)'
        )

    def handle(self, *args, **options):
        noinput = options['noinput']

        self.stdout.write(self.style.WARNING("Resetting the database..."))
        
        call_command('flush', interactive=not noinput)
        
        self.stdout.write(self.style.NOTICE("Making migrations..."))
        call_command('makemigrations')
        
        self.stdout.write(self.style.NOTICE("Applying migrations..."))
        call_command('migrate')
        
        if not noinput:
            create_super = input("Do you want to create a superuser now? (y/n): ").lower()
            if create_super == 'y':
                call_command('createsuperuser')
        else:
            self.stdout.write(self.style.WARNING("Skipping superuser creation in noinput mode"))

        self.stdout.write(self.style.SUCCESS("Database reset complete!"))
