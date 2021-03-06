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
        # print((request.user.is_anonymous))
        companies = CompanyUser.objects.all().order_by('-company_city')
        clients = ClientUser.objects.all().order_by('-date_create_client')
        context = {
            'companies': companies,
            'clients': clients
        }
        return render(request, 'all_users.html', context)


#### CRUD OPERATIONS ####

def crud_operations(request):
    # READ
    companies = CompanyUser.objects.filter(is_active=True)
    companies = (', ').join([companies[i].title for i in range(len(companies))])
    # CREATE
    client = ClientUser.objects.create(username='JohnyBobik', password='CrazyTop123')
    # UPDATE
    client.first_name = 'Jorszh'
    client.save()
    client1 = client
    client1.save()
    # DELETE
    client.delete()
    return HttpResponse(f'All CRUD operations was executed, {client1.first_name}, {client1.username}.'
                        f' Companies {companies} is ready')
