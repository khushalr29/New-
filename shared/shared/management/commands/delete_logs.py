import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Deletes individual API log files older than 10 days'

    def handle(self, *args, **kwargs):
        log_dir = settings.DRF_API_LOGGER_LOG_DIR
        if not os.path.exists(log_dir):
            self.stderr.write(self.style.ERROR(f"The log directory '{log_dir}' does not exist."))
            return
        
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
        current_time = time.time()
        for log_file in log_files:
            file_path = os.path.join(log_dir, log_file)
            try:
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > 10 * 24 * 60 * 60:
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f"Deleted log file: {log_file}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error deleting {log_file}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('API log cleanup completed.'))
