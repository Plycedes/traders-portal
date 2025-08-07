from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer
from .permissions import IsSuperUserOrReadOnly


class CompanyPagination(PageNumberPagination):
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


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of companies",
        parameters=[
            OpenApiParameter("page", type=int, location=OpenApiParameter.QUERY, required=False),
            OpenApiParameter("page_size", type=int, location=OpenApiParameter.QUERY, required=False),
            OpenApiParameter("search", type=str, location=OpenApiParameter.QUERY, description="Search companies by name, symbol or scripcode", required=False),
            OpenApiParameter("ordering", type=str, location=OpenApiParameter.QUERY, description="Order by company_name, symbol, or scripcode", required=False),
            OpenApiParameter("symbol", type=str, location=OpenApiParameter.QUERY, required=False),
            OpenApiParameter("scripcode", type=str, location=OpenApiParameter.QUERY, required=False),
            OpenApiParameter("company_name", type=str, location=OpenApiParameter.QUERY, required=False),
        ]
    ),
    retrieve=extend_schema(
        summary="Get details of a specific company by ID",
    ),
    create=extend_schema(
        summary="Create a new company",
        request=CompanySerializer,
    ),
    update=extend_schema(
        summary="Update all fields of a company by ID",
        request=CompanySerializer,
    ),
    partial_update=extend_schema(
        summary="Update one or more fields of a company by ID",
        request=CompanySerializer,
    ),
    destroy=extend_schema(
        summary="Delete a company by ID",
    )
)
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer
    permission_classes = [IsSuperUserOrReadOnly]
    pagination_class = CompanyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['symbol', 'scripcode', 'company_name']
    search_fields = ['symbol', 'scripcode', 'company_name']
    ordering_fields = ['company_name', 'symbol', 'scripcode']
