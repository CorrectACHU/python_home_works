from django.contrib import admin
from .models import ClientUser, CompanyUser, Order, Review, RatingStar, RatingCompany, Offer
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']
    list_display_links = ['username']


class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'date_create_client', 'first_name']
    list_display_links = ['user']
    fields = ['user','client_country', 'client_city']


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'username', 'first_name', 'date_create_company']
    fields = ['user', 'title', 'description', 'company_country', 'company_city', 'company_address',
              'pay_per_hour']
    list_display_links = ['title']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'head', 'body']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ClientUser, ClientUserAdmin)
admin.site.register(CompanyUser,CompanyUserAdmin)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(RatingStar)
admin.site.register(RatingCompany)
admin.site.register(Offer)
