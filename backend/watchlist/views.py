from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .models import UserWatchlist, WatchList
from companies.models import Company
from .serializers import UserWatchlistSerializer, WatchListItemSerializer


class WatchlistPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total_count': self.page.paginator.count,
            'count': len(data),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


@extend_schema(
    summary="Get all user's watchlists",
    description="Returns a list of all watchlists with their companies for the authenticated user.",
    responses={200: UserWatchlistSerializer(many=True)}
)
class UserWatchlistListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserWatchlistSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserWatchlist.objects.none()
        return UserWatchlist.objects.filter(user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Retrieve or delete a specific watchlist",
    description="Retrieve a watchlist with all its companies or delete it.",
    responses={200: UserWatchlistSerializer}
)
class UserWatchlistDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserWatchlistSerializer

    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)


@extend_schema(
    summary="Get companies in a specific watchlist",
    responses={200: WatchListItemSerializer(many=True)},
    parameters=[
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, required=False),
    ]
)
class WatchlistListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WatchListItemSerializer
    pagination_class = WatchlistPagination

    def get_queryset(self):
        watchlist_id = self.kwargs.get('watchlist_id')
        return WatchList.objects.filter(watchlist__id=watchlist_id, watchlist__user=self.request.user).order_by('id')


@extend_schema(
    summary="Add company to a specific watchlist",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "watchlist_id": {"type": "integer", "example": 1},
                "company_id": {"type": "integer", "example": 2}
            },
            "required": ["watchlist_id", "company_id"]
        }
    }
)
class AddToWatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        watchlist_id = request.data.get("watchlist_id")
        company_id = request.data.get("company_id")

        if not watchlist_id or not company_id:
            return Response({"error": "watchlist_id and company_id are required"}, status=400)

        try:
            watchlist = UserWatchlist.objects.get(id=watchlist_id, user=request.user)
        except UserWatchlist.DoesNotExist:
            return Response({"error": "Watchlist not found"}, status=404)

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)

        _, created = WatchList.objects.get_or_create(watchlist=watchlist, company=company)
        return Response(
            {"message": "Added to watchlist" if created else "Already in watchlist"},
            status=201 if created else 200
        )


@extend_schema(
    summary="Remove company from a specific watchlist",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "watchlist_id": {"type": "integer", "example": 1},
                "company_id": {"type": "integer", "example": 2}
            },
            "required": ["watchlist_id", "company_id"]
        }
    }
)
class RemoveFromWatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        watchlist_id = request.data.get("watchlist_id")
        company_id = request.data.get("company_id")

        if not watchlist_id or not company_id:
            return Response({"error": "watchlist_id and company_id are required"}, status=400)

        try:
            watchlist = UserWatchlist.objects.get(id=watchlist_id, user=request.user)
        except UserWatchlist.DoesNotExist:
            return Response({"error": "Watchlist not found"}, status=404)

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)

        deleted_count = WatchList.objects.filter(watchlist=watchlist, company=company).delete()[0]
        return Response(
            {"message": "Removed from watchlist" if deleted_count > 0 else "Already removed or never added"},
            status=200
        )
