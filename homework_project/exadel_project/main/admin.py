from django.contrib import admin
from .models import ClientUser, CompanyUser, Order, Review, RatingStar, RatingCompany, Offer, Profile
from django.contrib import admin


class ClientAdmin(admin.ModelAdmin):
    fields = ['user', 'client_country', 'client_city', 'rating']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'head', 'body']


admin.site.register(Profile)
admin.site.register(ClientUser,ClientAdmin)
admin.site.register(CompanyUser)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(RatingStar)
admin.site.register(RatingCompany)
admin.site.register(Offer)
