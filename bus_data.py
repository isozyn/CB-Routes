# bus_data.py
# Contains the bus route data and data-related functions

import json
import os

def load_routes_from_json(filename="routes.json"):
    """Load bus routes from a JSON file and convert to internal format."""
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            json_routes = json.load(jsonfile)
            
        converted_routes = []
        for route in json_routes:
            # Extract all stops from all legs
            all_stops = []
            
            # Add starting point from first leg
            if route['legs']:
                all_stops.append(route['legs'][0]['from'])
                
                # Add all intermediate and end points
                for leg in route['legs']:
                    # Parse stops from the leg if available
                    if 'stops' in leg and leg['stops'] and leg['stops'] != "See PDF":
                        # Split stops by semicolon and clean them
                        stops_in_leg = [stop.strip() for stop in leg['stops'].split(';')]
                        # Add stops that aren't already in the list
                        for stop in stops_in_leg:
                            if stop and stop not in all_stops:
                                all_stops.append(stop)
                    
                    # Always add the destination of this leg
                    if leg['to'] not in all_stops:
                        all_stops.append(leg['to'])
            
            # Estimate time and cost based on route complexity
            estimated_time = estimate_travel_time(route)
            estimated_cost = estimate_cost(route)
            
            converted_route = {
                'route_name': f"{route['route_id']} - {route['route_description']}",
                'stops': all_stops,
                'total_time': estimated_time,
                'total_cost': estimated_cost,
                'transfers': route.get('transfers_allowed', 0),
                'fare_code': route.get('fare_code', ''),
                'notes': route.get('notes', '')
            }
            converted_routes.append(converted_route)
        
        return converted_routes
        
    except FileNotFoundError:
        print(f"JSON file '{filename}' not found. Using sample data.")
        return get_sample_routes()
    except Exception as e:
        print(f"Error reading JSON file: {e}. Using sample data.")
        return get_sample_routes()

def estimate_travel_time(route):
    """Estimate travel time based on route complexity."""
    # Try to get real time from Google Maps if available
    try:
        from google_maps_integration import get_maps_integration
        maps = get_maps_integration()
        
        if maps and route.get('legs'):
            # Extract stops for Google Maps calculation
            all_stops = []
            if route['legs']:
                all_stops.append(route['legs'][0]['from'])
                for leg in route['legs']:
                    all_stops.append(leg['to'])
            
            if len(all_stops) >= 2:
                real_time = maps.calculate_route_time(all_stops)
                if real_time > 0:
                    return real_time
    except Exception as e:
        print(f"Google Maps integration failed, using estimation: {e}")
    
    # Fallback estimation
    base_time = 30  # Base time in minutes
    
    # Add time for each transfer
    transfer_time = route.get('transfers_allowed', 0) * 15
    
    # Add time based on number of legs
    leg_time = len(route.get('legs', [])) * 20
    
    return base_time + transfer_time + leg_time

def estimate_cost(route):
    """Estimate cost based on route information."""
    # Try to extract cost from fare information
    fare_info = route.get('through_cash_fare', '')
    
    # Look for R and number pattern
    import re
    cost_match = re.search(r'R(\d+(?:\.\d+)?)', fare_info)
    if cost_match:
        return float(cost_match.group(1))
    
    # Default estimation based on transfers
    base_cost = 15.0
    transfer_cost = route.get('transfers_allowed', 0) * 5.0
    
    return base_cost + transfer_cost

def get_sample_routes():
    """Return sample bus routes as fallback."""
    return [
        {
            'route_name': 'Route A',
            'stops': ['A', 'B', 'C', 'D'],
            'total_time': 40,  # in minutes
            'total_cost': 15   # in currency units
        },
        {
            'route_name': 'Route B',
            'stops': ['A', 'E', 'D'],
            'total_time': 35,
            'total_cost': 20
        },
        {
            'route_name': 'Route C',
            'stops': ['A', 'F', 'G', 'D'],
            'total_time': 50,
            'total_cost': 10
        }
    ]

# Load routes from JSON or use sample data
bus_routes = load_routes_from_json()

def get_all_stops():
    """Get all unique stops from all routes."""
    return sorted({stop for route in bus_routes for stop in route['stops']})

def get_routes():
    """Return all bus routes."""
    return bus_routes
