from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'scripcode', 'company_name')
    search_fields = ('symbol', 'scripcode', 'company_name')
    list_filter = ('symbol', 'company_name')
