from datetime import timezone

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import ClientUser, CompanyUser


def base_view(request):
    return HttpResponse('Hello! This view works')


class ListClientView(ListView):
    model = ClientUser
    template_name = 'list_clients.html'


class DetailUserView(DetailView):
    model = ClientUser
    template_name = 'detail_client.html'


class CompaniesView(View):
    def get(self, request):
        companies = CompanyUser.objects.all().order_by('-company_city')
        context = {
            'companies': companies
        }
        return render(request, 'companies_list.html', context)


class AllUsersView(View):
    def get(self, request):
        companies = CompanyUser.objects.all().order_by('-company_city')
        clients = ClientUser.objects.all().order_by('-date_create_client')
        context = {
            'companies': companies,
            'clients': clients
        }
        return render(request, 'all_users.html', context)
