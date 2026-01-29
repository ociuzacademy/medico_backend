from django.db import models

# Create your models here.
class tbl_admin(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    email = models.EmailField()

    def __str__(self):
        return self.username
    

