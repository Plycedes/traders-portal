from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20, blank=True, null=True)
    scripcode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.symbol})"
