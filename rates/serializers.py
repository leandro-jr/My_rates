# rates/serializers.py
from rest_framework import serializers
from .models import MoviesRates, MoviesData

class MoviesRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviesRates
        fields = ["id", "filme", "nota", "data"]


class MoviesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviesData
        fields = '__all__'