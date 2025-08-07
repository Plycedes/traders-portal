from django.urls import path
from .views import WatchlistListView, AddToWatchlistView, RemoveFromWatchlistView

urlpatterns = [
    path('', WatchlistListView.as_view(), name='watchlist-list'),
    path('add/', AddToWatchlistView.as_view(), name='watchlist-add'),
    path('remove/', RemoveFromWatchlistView.as_view(), name='watchlist-remove')
]