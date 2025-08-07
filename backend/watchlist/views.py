from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import WatchList
from companies.models import Company
from .serializers import WatchListSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class WatchlistPagination(PageNumberPagination):
    page_size=10
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
    summary="Get user's watchlist",
    description="Returns a paginated list of companies in the authenticated user's watchlist.",
    responses={200: WatchListSerializer(many=True)},
    parameters=[
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, required=False),
    ],      
)
class WatchlistListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WatchListSerializer
    pagination_class = WatchlistPagination
    
    def get_queryset(self):
        # Handle schema generation when user is anonymous
        if getattr(self, 'swagger_fake_view', False):
            return WatchList.objects.none()
        
        # Handle case where user might not be authenticated
        if not self.request.user.is_authenticated:
            return WatchList.objects.none()
            
        return WatchList.objects.filter(user=self.request.user).order_by('id')

@extend_schema(
    summary="Add company to watchlist",
    description="Adds a company to the authenticated user's watchlist. If already present, returns a message accordingly.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "company_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "ID of the company to add"
                }
            },
            "required": ["company_id"]
        }
    },
    responses={
        201: OpenApiResponse(description="Company successfully added to watchlist"),
        200: OpenApiResponse(description="Company was already in watchlist"),
        400: OpenApiResponse(description="company_id is required"),
        404: OpenApiResponse(description="Company not found")
    }
)
class AddToWatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        company_id = request.data.get("company_id")
        if not company_id:
            return Response({"error": "company_id is required"}, status=400)
        
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)
        
        _, created = WatchList.objects.get_or_create(user=request.user, company=company)
        return Response(
            {"message": "Added to watchlist" if created else "Already in watchlist"},
            status=201 if created else 200
        )

@extend_schema(
    summary="Remove company from watchlist",
    description="Removes a company from the authenticated user's watchlist. If not present, returns appropriate message.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "company_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "ID of the company to remove"
                }
            },
            "required": ["company_id"]
        }
    },
    responses={
        200: OpenApiResponse(description="Removed from watchlist or already removed"),
        400: OpenApiResponse(description="company_id is required"),
        404: OpenApiResponse(description="Company not found")
    }
)    
class RemoveFromWatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        company_id = request.data.get("company_id")
        if not company_id:
            return Response({"error": "company_id is required"}, status=400)
        
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)
        
        deleted_count = WatchList.objects.filter(user=request.user, company=company).delete()[0]
        return Response(
            {"message": "Removed from watchlist" if deleted_count > 0 else "Already removed from watchlist or was never added"},
            status=200
        )
