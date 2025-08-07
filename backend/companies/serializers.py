from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=True)
    symbol = serializers.CharField(required=False, allow_blank=True)
    scripcode = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'symbol', 'scripcode']
