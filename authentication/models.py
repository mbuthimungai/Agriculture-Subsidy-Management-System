from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(db_index=True)
    password = models.CharField(db_index=True)
    
