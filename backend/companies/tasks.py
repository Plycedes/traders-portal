from celery import shared_task
import random
from .models import Company

@shared_task
def update_company_prices():
    companies = Company.objects.all()
    for company in companies:
        # Simulate price update
        company.scripcode = str(random.randint(100000, 999999))
        company.save()
    return f"Updated {companies.count()} companies."
