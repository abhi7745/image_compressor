from django.db import models

# Create your models here.

class image_handler(models.Model):
    my_id=models.AutoField(primary_key=True)
    user_image=models.ImageField(upload_to="")