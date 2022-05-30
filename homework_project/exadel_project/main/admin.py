from django.contrib import admin
from django.contrib.auth.models import User

from .models import ClientUser, CompanyUser, Order, Comment, RatingStar, RatingCompany, Offer
from django.contrib import admin




# class ClientAdmin(admin.ModelAdmin):
#     fields = ['user', 'client_country', 'client_city']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'head', 'body']


admin.site.register(ClientUser)
admin.site.register(CompanyUser)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(RatingStar)
admin.site.register(RatingCompany)
admin.site.register(Offer)
