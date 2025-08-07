from django.contrib import admin
from .models import WatchList

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'created_at')
    list_filter = ('created_at', 'company')
    search_fields = ('user__username', 'company__company_name')
    ordering = ('-created_at',)
