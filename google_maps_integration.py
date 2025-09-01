# google_maps_integration.py
# Google Maps API integration for real distance and time calculations

import requests
import json
from typing import List, Dict, Tuple

class GoogleMapsIntegration:
    def __init__(self, api_key: str):
        """Initialize with Google Maps API key."""
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api"
    
    def get_distance_matrix(self, origins: List[str], destinations: List[str]) -> Dict:
        """Get distance and duration between multiple origins and destinations."""
        url = f"{self.base_url}/distancematrix/json"
        
        params = {
            'origins': '|'.join(origins),
            'destinations': '|'.join(destinations),
            'mode': 'transit',  # Use public transport
            'transit_mode': 'bus',
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Error getting distance matrix: {e}")
            return {}
    
    def calculate_route_time(self, stops: List[str]) -> int:
        """Calculate total travel time for a route with multiple stops."""
        if len(stops) < 2:
            return 0
        
        total_time = 0
        
        for i in range(len(stops) - 1):
            origin = stops[i]
            destination = stops[i + 1]
            
            result = self.get_distance_matrix([origin], [destination])
            
            if (result.get('status') == 'OK' and 
                result.get('rows') and 
                result['rows'][0].get('elements') and
                result['rows'][0]['elements'][0].get('status') == 'OK'):
                
                duration = result['rows'][0]['elements'][0]['duration']['value']
                total_time += duration // 60  # Convert seconds to minutes
            else:
                # Fallback estimation if API fails
                total_time += 15  # Assume 15 minutes per segment
        
        return total_time
    
    def get_route_coordinates(self, stops: List[str]) -> List[Tuple[float, float]]:
        """Get latitude/longitude coordinates for each stop."""
        coordinates = []
        
        for stop in stops:
            url = f"{self.base_url}/geocode/json"
            params = {
                'address': stop + ", Cape Town, South Africa",
                'key': self.api_key
            }
            
            try:
                response = requests.get(url, params=params)
                data = response.json()
                
                if data.get('status') == 'OK' and data.get('results'):
                    location = data['results'][0]['geometry']['location']
                    coordinates.append((location['lat'], location['lng']))
                else:
                    coordinates.append((0, 0))  # Default if geocoding fails
            except:
                coordinates.append((0, 0))
        
        return coordinates

# Configuration - You need to get a Google Maps API key
GOOGLE_MAPS_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key

def get_maps_integration():
    """Get Google Maps integration instance."""
    if GOOGLE_MAPS_API_KEY != "YOUR_API_KEY_HERE":
        return GoogleMapsIntegration(GOOGLE_MAPS_API_KEY)
    return None
