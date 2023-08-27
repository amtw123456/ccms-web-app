from djongo import models

class DailyCasePriceHistoryInformation(models.Model):
    caseName = models.CharField(max_length=100)
    currentTimeCreatedInUtc = models.DateTimeField()
    casePriceHistoryDaily = models.JSONField(default=list)

    def __str__(self):
        return self.caseName