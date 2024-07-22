from django.db import models

# Create your models here.

class Membres(models.Model):
    Pseudo = models.CharField(max_length=20)
    email = models.EmailField()
    photo = models.ImageField(upload_to="static/img/img_user")
    pwd = models.TextField()

