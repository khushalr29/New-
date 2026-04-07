import os
import datetime
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Backs up the PostgreSQL database to a .sql file'

    def handle(self, *args, **options):

        db = settings.DATABASES['default']
        db_name = db['NAME']
        db_user = db['USER']
        db_password = db['PASSWORD']
        db_host = db.get('HOST', 'localhost')
        db_port = db.get('PORT', '5432')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{db_name}_backup_{timestamp}.sql"
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        filepath = os.path.join(backup_dir, filename)
        self.stdout.write(f"Backing up database to: {filepath}")
        os.environ['PGPASSWORD'] = db_password

        try:
            subprocess.run([
                'pg_dump',
                '-h', db_host,
                '-p', db_port,
                '-U', db_user,
                '-f', filepath,
                db_name
            ], check=True)
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("Backup failed!"))
            self.stderr.write(str(e))
            return
        
        self.stdout.write(self.style.SUCCESS("Backup completed successfully."))
