from django.db import models
from django.conf import settings
from companies.models import Company

class WatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='watchlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company')
    
    def __str__(self):
        return f"{self.user.username} - {self.company.company_name}"
