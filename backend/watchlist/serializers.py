from rest_framework import serializers
from .models import WatchList, UserWatchlist
from companies.serializers import CompanySerializer

class WatchListItemSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = WatchList
        fields = ['id', 'company', 'created_at']


class UserWatchlistSerializer(serializers.ModelSerializer):
    items = WatchListItemSerializer(many=True, read_only=True)

    class Meta:
        model = UserWatchlist
        fields = ['id', 'name', 'created_at', 'items']
