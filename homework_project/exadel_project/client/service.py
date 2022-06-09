from django_filters import rest_framework as filters
from main.models import CompanyUser


# class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass

class CompaniesFilter(filters.FilterSet):
    avg_rating = filters.RangeFilter()

    class Meta:
        model = CompanyUser
        fields = ['avg_rating']
