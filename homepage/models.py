from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TravelPlans(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    place_id=models.IntegerField()

    def __str__(self):
        return str(self.user)+"--"+str(self.place_id)