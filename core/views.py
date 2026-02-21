from rest_framework import generics, filters
from django.db.models import Min
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import TruckStop, RackPrice
from core.serializers import TruckStopSerializer
import requests
from django.conf import settings

MAX_RANGE_MILES = 500
FUEL_EFFICIENCY_MPG = 10  # miles per gallon
ORS_API_KEY = settings.ORS_API_KEY  # get free key

class TruckStopListView(generics.ListAPIView):
    queryset = TruckStop.objects.annotate(
        min_price=Min('rack_prices__retail_price')
    )
    serializer_class = TruckStopSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["city", "state"]
    ordering_fields = ["city", "min_price"]
    ordering = ["city"]

@api_view(['GET'])
def route_with_fuel_stops(request):
    start = request.GET.get('start')  # "lng,lat"
    finish = request.GET.get('finish')

    if not start or not finish:
        return Response({"error": "Start and finish parameters are required."}, status=400)

    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY}
    params = {"start": start.replace(" ", ""), "end": finish.replace(" ", "")}

    route_response = requests.get(ors_url, headers=headers, params=params)
    if route_response.status_code != 200:
        return Response({"error": "Failed to get route from API."}, status=500)

    route_data = route_response.json()
    total_distance_m = route_data['features'][0]['properties']['segments'][0]['distance']
    total_distance_miles = total_distance_m * 0.000621371

    num_stops = int(total_distance_miles // MAX_RANGE_MILES) + 1

    cheapest_rack_prices = (
        RackPrice.objects.select_related('truckstop')
        .order_by('retail_price')[:num_stops]
    )

    stops_data = [
        {
            "truckstop_name": rack.truckstop.name,
            "city": rack.truckstop.city,
            "state": rack.truckstop.state,
            "rack_id": rack.rack_id,
            "price": float(rack.retail_price),
            "latitude": rack.truckstop.latitude,
            "longitude": rack.truckstop.longitude
        }
        for rack in cheapest_rack_prices
    ]

    total_gallons_needed = total_distance_miles / FUEL_EFFICIENCY_MPG
    total_cost = total_gallons_needed * float(cheapest_rack_prices[0].retail_price) if cheapest_rack_prices else 0

    return Response({
        "route_distance_miles": total_distance_miles,
        "fuel_stops": stops_data,
        "total_cost": total_cost,
        "route_map_url": f"https://www.openstreetmap.org/directions?from={start}&to={finish}"
    })