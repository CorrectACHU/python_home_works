from django.db import models
from django.contrib.auth.models import User


class ClientUser(models.Model):
    """ Instances of clients"""
    profile = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='client')
    nick = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    client_country = models.CharField(max_length=25, null=True, blank=True)
    client_city = models.CharField(max_length=30, null=True, blank=True)
    date_create_client = models.DateTimeField(auto_now_add=True)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nick}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class CompanyUser(models.Model):
    """ Instances of Companies """
    profile_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='company')
    title = models.CharField(max_length=20)
    description = models.TextField()
    phone = models.CharField(max_length=30)
    company_country = models.CharField(max_length=25)
    company_city = models.CharField(max_length=30)
    company_address = models.CharField(max_length=100, null=True, blank=True)
    pay_per_hour = models.DecimalField(max_digits=4, decimal_places=2)
    date_create_company = models.DateTimeField(auto_now_add=True)
    is_company = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Order(models.Model):
    """ Instances of client Orders """
    STATUS_CHOICE = [
        ('open', 'open'),
        ('in_process', 'in_process'),
        ('closed', 'closed')
    ]

    client_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    notified_companies = models.ManyToManyField(CompanyUser, related_name='orders')
    head = models.CharField(max_length=50)
    body = models.TextField()
    country = models.CharField(max_length=25)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    house_door = models.CharField(max_length=30)
    square_in_meters = models.IntegerField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default='open')
    accepted_offer = models.IntegerField(null=True, blank=True)
    date_create_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.head}'


class Offer(models.Model):
    """ Instances of companies offers for clients """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='offer_id')
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='company_id')
    price = models.IntegerField()
    is_accepted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'order:{self.order.head}////  Company:{self.company.title}'


class RatingStar(models.Model):
    """ Instances of our stars for Rating model """
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.value}'


class RatingCompany(models.Model):
    """ Instances of company ratings """
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='evaluations')
    client_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE, related_name='rating_owner')
    star_value = models.ForeignKey(RatingStar, on_delete=models.CASCADE, related_name='rating_stars')
    date_create_rating = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_owner} add rating {self.star_value} *stars* to {self.company.title} '


class Comment(models.Model):
    """ Instances of company reviews """
    client_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE, related_name='comment_owner')
    company_id = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='reviews')
    header = models.CharField(max_length=50)
    text = models.TextField()
    date_create_review = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_owner} {self.company_id}'
