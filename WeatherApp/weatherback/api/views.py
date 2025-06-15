import os
import requests
from decouple import config
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
api_key = config('WEATHER_API_KEY')
url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
params = {
    'key': api_key,
    'elements': 'datetime,tempmax,tempmin,temp,sunrise,sunset',
    'include': 'days',
    'unitGroup': 'metric'
}


@api_view(['GET'])
def weather_info(request, location):
    cache_key = f'weather_info_for : {location}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data, status=200)
    # If not cached, fetch the data from the API
    try:
        response = requests.get(url + location, params=params)
        data = response.json()
        if response.status_code == 200:
            weather_data = data.get('days', [])
            if not weather_data:
                return Response({'error': 'No weather data found for the specified location.'}, status=404)
            
            # Extracting the first day's weather data
            day_data = weather_data[0]
            result = {
                'real location': data.get('resolvedAddress', 'Unknown Location'),
                'location': data.get('address', 'Unknown Location'),
                'date': day_data.get('datetime'),
                'max_temp': day_data.get('tempmax'),
                'min_temp': day_data.get('tempmin'),
                'avg_temp': day_data.get('temp'),
                'sunrise': day_data.get('sunrise'),
                'sunset': day_data.get('sunset')
            }
            cache.set(cache_key, result, timeout=60*60)
            # Return the result as a JSON response
            return Response(result, status=200)
        else:
            return Response({'error': f'Error fetching data: {data.get("message", "Unknown error")}'}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Failed to connect to the weather service.\n{str(e)}'}, status=500)
