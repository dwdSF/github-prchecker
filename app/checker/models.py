from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Check(models.Model):
    ''' Comment here '''

    project_name = models.CharField(max_length=150)
    stars_number = models.IntegerField()
    url = models.CharField(max_length=150)
    merged_prs = models.TextField()
    not_merged_prs = models.TextField()
    username = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.project_name)
