from django.db import models


class Products(models.Model):

    title = models.CharField(max_length=255, db_index=True)
    price = models.IntegerField(db_index=True)
    photo = models.ImageField(upload_to='products_icons/')