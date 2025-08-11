from django.urls import path
from .views import (
    UserWatchlistListCreateView,
    UserWatchlistDetailView,
    WatchlistListView,
    AddToWatchlistView,
    RemoveFromWatchlistView
)

urlpatterns = [
    # User's watchlists
    path('lists/', UserWatchlistListCreateView.as_view(), name='user-watchlist-list-create'),
    path('lists/<int:pk>/', UserWatchlistDetailView.as_view(), name='user-watchlist-detail'),

    # Companies in a watchlist
    path('lists/<int:watchlist_id>/items/', WatchlistListView.as_view(), name='watchlist-items'),

    # Add/remove company in watchlist
    path('lists/items/add/', AddToWatchlistView.as_view(), name='watchlist-item-add'),
    path('lists/items/remove/', RemoveFromWatchlistView.as_view(), name='watchlist-item-remove'),
]
