from django.core.management.base import BaseCommand
from django.db import connection, transaction
import os
import re

class Command(BaseCommand):
    help = 'Seeds static data for countries, states, cities, etc.'

    def handle(self, *args, **kwargs):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static_sql'))
        files = ['regions.sql', 'subregions.sql', 'countries.sql', 'states.sql', 'cities.sql', 'world.sql','currency.sql']

        drop_constraint_pattern = re.compile(
            r'(ALTER\s+TABLE\s+.+?\s+DROP\s+CONSTRAINT\s+.+?)(;)', 
            re.IGNORECASE | re.DOTALL)
        drop_table_pattern = re.compile(
            r'(DROP\s+TABLE\s+.+?)(;)', 
            re.IGNORECASE | re.DOTALL)

        for file_name in files:
            file_path = os.path.join(base_dir, file_name)
            self.stdout.write(f"Running {file_name}...")

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                filtered_lines = []
                for line in content.splitlines():
                    stripped = line.strip()
                    if (not stripped or
                        stripped.startswith('--') or
                        stripped.startswith('Type:') or
                        stripped.startswith('Name:') or
                        stripped.startswith('Schema:')):
                        continue
                    filtered_lines.append(line)

                filtered_sql = '\n'.join(filtered_lines)

                if not filtered_sql.strip():
                    self.stdout.write(self.style.WARNING(f"Skipped {file_name}: no valid SQL found."))
                    continue

                def add_cascade(match):
                    statement = match.group(1).strip()
                    semicolon = match.group(2)

                    if not statement.upper().endswith('CASCADE'):
                        statement += ' CASCADE'

                    return statement + semicolon

                filtered_sql = drop_constraint_pattern.sub(add_cascade, filtered_sql)

                filtered_sql = drop_table_pattern.sub(add_cascade, filtered_sql)

                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute(filtered_sql)

                self.stdout.write(self.style.SUCCESS(f"Successfully executed {file_name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in {file_name}: {e}"))
