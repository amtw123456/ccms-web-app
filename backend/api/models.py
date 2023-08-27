from djongo import models
from rest_framework import serializers

class DailyPriceData(models.Model):
    date = models.CharField(max_length=100)
    casePrice = models.DecimalField(max_digits=10, decimal_places=3)
    numOfCaseSold = models.IntegerField()

class DailyCasePriceHistoryInformation(models.Model):
    caseName = models.CharField(max_length=100)
    currentTimeCreatedInUtc = models.DateTimeField()
    casePriceHistoryDaily = models.JSONField(default=list)

    def __str__(self):
        return self.caseName