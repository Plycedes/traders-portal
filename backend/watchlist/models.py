from django.db import models
from django.conf import settings
from companies.models import Company

class UserWatchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class WatchList(models.Model):
    watchlist = models.ForeignKey(UserWatchlist, on_delete=models.CASCADE, related_name='items')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='in_watchlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('watchlist', 'company')

    def __str__(self):
        return f"{self.watchlist.name} - {self.company.company_name}"

