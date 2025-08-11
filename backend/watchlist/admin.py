from django.contrib import admin
from .models import UserWatchlist, WatchList


class WatchListInline(admin.TabularInline):
    model = WatchList
    extra = 1
    autocomplete_fields = ['company']  # Makes selecting companies easier


@admin.register(UserWatchlist)
class UserWatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created_at')
    search_fields = ('user__username', 'name')
    list_filter = ('created_at',)
    inlines = [WatchListInline]


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ('id', 'watchlist', 'company', 'created_at')
    search_fields = ('watchlist__name', 'company__company_name')
    list_filter = ('created_at', 'company')
    autocomplete_fields = ['watchlist', 'company']
