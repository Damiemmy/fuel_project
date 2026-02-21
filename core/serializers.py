# core/serializers.py
from rest_framework import serializers
from .models import TruckStop, RackPrice

class RackPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RackPrice
        fields = ("rack_id", "retail_price")

class TruckStopSerializer(serializers.ModelSerializer):
    rack_prices = RackPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = TruckStop
        fields = (
            "opis_truckstop_id",
            "name",
            "address",
            "city",
            "state",
            "latitude",
            "longitude",
            "rack_prices"
        )