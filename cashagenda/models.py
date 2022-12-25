from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    avatar = models.ImageField(upload_to="user_avatars/")
    
    def __str__(self):
        return self.username