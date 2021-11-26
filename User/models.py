from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    on_hold_user = models.BooleanField()
    confirmation_code = models.IntegerField(default=None, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)
    
    