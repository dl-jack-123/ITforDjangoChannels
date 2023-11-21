# chat/models.py
from django.db import models

# Create your models here.


class Product(models.Model):
    date = models.DateField()
    type = models.CharField(max_length = 30)
    exchange = models.CharField(max_length = 30)
    market = models.CharField(max_length = 30)
    industry = models.CharField(max_length = 30)
    isnormal = models.BooleanField()
    isattention = models.BooleanField()
    isdisposition = models.BooleanField()
    ishalted = models.BooleanField()
    symbol = models.CharField(max_length = 30)
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f'{self.date},{self.exchange},{self.symbol}'


class Quote(models.Model):
    datetime = models.DateTimeField()
    symbol = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    referencePrice = models.FloatField()
    openPrice = models.FloatField()
    highPrice = models.FloatField()
    lowPrice = models.FloatField()
    closePrice = models.FloatField()
    avgPrice = models.FloatField()
    lastSize = models.IntegerField()

    class Meta:
        db_table = 'quote'

    def __str__(self):
        return f'{self.datetime},{self.symbol},{self.name}'

