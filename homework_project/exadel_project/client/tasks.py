from main.models import ClientUser

from exadel_project.celery import app


@app.task
def count_clients():
    count = ClientUser.objects.count()
    return count, 's'*20

