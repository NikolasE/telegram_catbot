from django.db import models


# we simply count the number of cat images we sent to a person
# (we use first name as user_id which will create collisions, but also adds privacy by design)
class UserLog(models.Model):
    user_id = models.CharField(max_length=100)
    cat_count = models.IntegerField(default=0)
