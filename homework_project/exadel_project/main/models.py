from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'


class ClientUser(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, related_name='client')
    client_country = models.CharField(max_length=25, null=True, blank=True)
    client_city = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=25)
    rating = models.IntegerField(default=0)
    date_create_client = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user.username}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class CompanyUser(models.Model):
    '''Instances of our Companies'''
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, related_name='company')
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
    '''Instances of clients Orders'''
    STATUS_CHOICE = [
        ('1', 'open'),
        ('2', 'in_process'),
        ('3', 'closed')
    ]

    client_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    head = models.CharField(max_length=50)
    body = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default='open')
    square_in_meters = models.IntegerField()
    date_create_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.head}'


class Offer(models.Model):
    '''Instances of Companies offers for clients'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_offer')
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)


class RatingStar(models.Model):
    '''Instances of our stars for Rating model'''
    value = models.SmallIntegerField()

    def __str__(self):
        return f'{self.value}'


class RatingCompany(models.Model):
    '''Instances of company ratings'''
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='evaluations')
    rating_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    star_value = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    date_create_rating = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating_owner} {self.company} {self.star_value}'


class Review(models.Model):
    '''Instances of company reviews'''
    review_owner = models.ForeignKey(ClientUser, on_delete=models.CASCADE, related_name='review_owner_client')
    review_company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='review_company_getter')
    header = models.CharField(max_length=50)
    text = models.TextField()
    date_create_review = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.review_owner} {self.review_company}'
