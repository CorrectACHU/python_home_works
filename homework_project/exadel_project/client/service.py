from django_filters import rest_framework as filters
from main.models import CompanyUser


class CompaniesFilter(filters.FilterSet):
    avg_rating = filters.RangeFilter()

    class Meta:
        model = CompanyUser
        fields = ['avg_rating']
