from django.db import models

# Create your models here.


class UserLog(models.Model):
    user_id = models.CharField(max_length=100)
    cat_count = models.IntegerField(default=0)
