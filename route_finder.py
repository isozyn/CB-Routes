# route_finder.py
# Contains the logic for finding and comparing routes

from bus_data import get_routes

def find_routes(start, end):
    """Find all routes that go from start to end."""
    valid_routes = []
    routes = get_routes()
    
    for route in routes:
        if start in route['stops'] and end in route['stops']:
            start_idx = route['stops'].index(start)
            end_idx = route['stops'].index(end)
            if start_idx < end_idx:
                valid_routes.append(route)
    return valid_routes

def get_fastest_route(routes):
    """Get the route with the shortest travel time."""
    return min(routes, key=lambda r: r['total_time']) if routes else None

def get_cheapest_route(routes):
    """Get the route with the lowest cost."""
    return min(routes, key=lambda r: r['total_cost']) if routes else None
