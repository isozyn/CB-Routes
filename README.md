# Bus Route Comparator - Week 7 Project

This project compares different bus routes to find the fastest and cheapest options between two locations.

## Project Structure

```
CB-Routes/
├── main.py          # Main entry point - run this file
├── gui.py           # Tkinter GUI interface
├── route_finder.py  # Route comparison logic
├── bus_data.py      # Bus route data and data functions
└── README.md        # This file
```

## File Descriptions

### `main.py`
- Main entry point for the application
- Handles error catching and starts the GUI

### `gui.py`
- Contains the Tkinter GUI interface
- Handles user input and displays results
- Creates dropdown menus for location selection
- Shows route comparison results

### `route_finder.py`
- Contains the core logic for finding routes
- Functions to find fastest and cheapest routes
- Route filtering based on start/end locations

### `bus_data.py`
- Contains sample bus route data
- Data structure with route names, stops, times, and costs
- Helper functions to access route data

## How to Run

1. Make sure you have Python installed with Tkinter (comes with most Python installations)
2. Navigate to the project directory
3. Run: `python main.py`

## How to Use

1. Select your starting location from the first dropdown menu
2. Select your destination from the second dropdown menu
3. Click "Find Routes" to see all available routes
4. The results will show:
   - All available routes between your selected locations
   - The fastest route (shortest time)
   - The cheapest route (lowest cost)

## Features

- User-friendly GUI interface
- Input validation and error handling
- Displays all routes with detailed information
- Highlights the best options (fastest and cheapest)
- Scrollable results area for long lists

## Sample Data

The project includes sample routes with stops labeled A through G, with different times and costs for demonstration purposes. You can modify the data in `bus_data.py` to add your own routes.
