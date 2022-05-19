from django.test import TestCase

from main.models import CompanyUser

from homework_project.exadel_project.main.models import ClientUser

count = 0


def create_companies(x, y, z, t):
    c = CompanyUser.objects.create_user(username=x ,password=y,email=z, title=t)
    c.save()
    global count
    if count < 15:
        count += 1
        create_companies(x + 'I', y, '1' + z, 'O'+t)
    return 'All okay'


create_companies('Cleaning_heaven', 'Futurama1', 'ssspolozmale@mail.ru', 'cleanAnd')

count = 0


def create_clinets(x, y, z):
    c = ClientUser.objects.create_user(username=x, password=y, email=z)
    c.save()
    global count
    if count < 15:
        count += 1
        create_clinets(x + 'I', y, '1' + z)
    return 'All okay'


create_clinets('Johny', 'Futurama1', 'keyfear@mail.ru')
