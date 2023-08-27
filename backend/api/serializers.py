from rest_framework import serializers
from .models import *

class DailyCasePriceHistoryInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCasePriceHistoryInformation
        fields = '__all__'
