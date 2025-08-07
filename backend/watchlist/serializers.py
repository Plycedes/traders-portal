from rest_framework import serializers
from .models import WatchList
from companies.serializers import CompanySerializer

class WatchListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = WatchList
        fields = ['id', 'company', 'created_at']