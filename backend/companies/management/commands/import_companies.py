import csv
from django.core.management.base import BaseCommand
from companies.models import Company

class Command(BaseCommand):
    help = 'Import companies from CSV'

    def handle(self, *args, **kwargs):
        with open('companies.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            companies = []
            for row in reader:
                if row['company_name']:  # Ensure required field is present
                    companies.append(Company(
                        company_name=row['company_name'],
                        symbol=row.get('symbol', '') or None,
                        scripcode=row.get('scripcode', '') or None
                    ))
            Company.objects.bulk_create(companies, batch_size=1000)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(companies)} companies'))
