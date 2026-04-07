from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs makemigrations and migrate together'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Running makemigrations..."))
        call_command('makemigrations')
        
        self.stdout.write(self.style.NOTICE("Running migrate..."))
        call_command('migrate')
        
        self.stdout.write(self.style.SUCCESS("All migrations applied successfully!"))
