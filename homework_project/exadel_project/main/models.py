from django.db import models
from django.contrib.auth.models import User


class ClientUser(User):
    client_country = models.CharField(max_length=25, null=True, blank=True)
    client_city = models.CharField(max_length=30, null=True, blank=True)
    date_create_client = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class CompanyUser(User):
    title = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    company_country = models.CharField(max_length=25, null=True, blank=True)
    company_city = models.CharField(max_length=30, null=True, blank=True)
    company_address = models.CharField(max_length=100, null=True, blank=True)
    pay_per_hour = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    date_create_company = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Order(models.Model):
    STATUS_CHOICE = [
        ('1', 'open'),
        ('2', 'in_process'),
        ('3', 'closed')
    ]

    client_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    companies = models.ManyToManyField(CompanyUser, related_name='possible_companies', blank=True, null=True)
    head = models.CharField(max_length=50)
    body = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default=None)
    square_in_meters = models.IntegerField()
    date_create_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.head}'


class RatingStar(models.Model):
    value = models.SmallIntegerField()

    def __str__(self):
        return f'{self.value}'


class RatingCompany(models.Model):
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    rating_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    star_value = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    date_create_rating = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating_owner} {self.company} {self.star_value}'


class Review(models.Model):
    review_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating_company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    text = models.TextField()
    date_create_review = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.review_owner} {self.rating_company}'
