from django.contrib import admin
from .models import ClientUser, CompanyUser, Order, Review, RatingStar, RatingCompany


class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'first_name', 'last_name', 'date_create_client']
    fields = ['username', 'password', 'first_name', 'last_name', 'client_country', 'client_city']


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'date_create_company']
    fields = ['username', 'password', 'title', 'description', 'company_country', 'company_city', 'company_address',
              'pay_per_hour']


admin.site.register(ClientUser, ClientUserAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(RatingStar)
admin.site.register(RatingCompany)
