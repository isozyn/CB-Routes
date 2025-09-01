# gui.py
# Contains the Tkinter GUI interface

import tkinter as tk
from tkinter import ttk, messagebox
from bus_data import get_all_stops
from route_finder import find_routes, get_fastest_route, get_cheapest_route

class BusRouteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Route Comparator")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Get all unique stops
        self.all_stops = get_all_stops()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Bus Route Comparator", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10)
        
        # Start location
        tk.Label(input_frame, text="Starting Location:", font=("Arial", 10), bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(input_frame, textvariable=self.start_var, values=self.all_stops, width=15)
        self.start_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # End location
        tk.Label(input_frame, text="Destination:", font=("Arial", 10), bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.end_var = tk.StringVar()
        self.end_combo = ttk.Combobox(input_frame, textvariable=self.end_var, values=self.all_stops, width=15)
        self.end_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Search button
        search_btn = tk.Button(input_frame, text="Find Routes", command=self.search_routes,
                              bg='#4CAF50', fg='white', font=("Arial", 10, "bold"), width=15)
        search_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Google Maps button
        maps_btn = tk.Button(input_frame, text="View on Google Maps", command=self.open_google_maps,
                            bg='#2196F3', fg='white', font=("Arial", 10, "bold"), width=15)
        maps_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Results frame
        results_frame = tk.Frame(self.root, bg='#f0f0f0')
        results_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Results text area with scrollbar
        self.results_text = tk.Text(results_frame, height=15, width=70, font=("Courier", 10),
                                   wrap=tk.WORD, bg='white', relief='sunken', bd=2)
        scrollbar = tk.Scrollbar(results_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initial message
        self.results_text.insert(tk.END, "Welcome to the Bus Route Comparator!\n\n")
        self.results_text.insert(tk.END, f"Available stops: {', '.join(self.all_stops)}\n\n")
        self.results_text.insert(tk.END, "Please select your starting location and destination, then click 'Find Routes'.")
        self.results_text.config(state='disabled')
    
    def search_routes(self):
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()
        
        # Validation
        if not start or not end:
            messagebox.showerror("Error", "Please select both starting location and destination.")
            return
        
        if start == end:
            messagebox.showerror("Error", "Starting location and destination cannot be the same.")
            return
        
        if start not in self.all_stops or end not in self.all_stops:
            messagebox.showerror("Error", "Please select valid locations from the dropdown.")
            return
        
        # Clear previous results
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        # Find routes
        routes = find_routes(start, end)
        
        if not routes:
            self.results_text.insert(tk.END, f"No routes found from {start} to {end}.\n")
            self.results_text.insert(tk.END, "Please try different locations.")
        else:
            fastest = get_fastest_route(routes)
            cheapest = get_cheapest_route(routes)
            
            self.results_text.insert(tk.END, f"Route search: {start} → {end}\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            
            # Show all available routes
            self.results_text.insert(tk.END, "ALL AVAILABLE ROUTES:\n")
            self.results_text.insert(tk.END, "-" * 30 + "\n")
            for i, route in enumerate(routes, 1):
                self.results_text.insert(tk.END, f"{i}. {route['route_name']}\n")
                self.results_text.insert(tk.END, f"   Stops: {' → '.join(route['stops'])}\n")
                self.results_text.insert(tk.END, f"   Time: {route['total_time']} minutes\n")
                self.results_text.insert(tk.END, f"   Cost: ${route['total_cost']}\n\n")
            
            # Show best options
            self.results_text.insert(tk.END, "BEST OPTIONS:\n")
            self.results_text.insert(tk.END, "=" * 20 + "\n")
            
            if fastest:
                self.results_text.insert(tk.END, "🚀 FASTEST ROUTE:\n")
                self.results_text.insert(tk.END, f"   {fastest['route_name']}\n")
                self.results_text.insert(tk.END, f"   Stops: {' → '.join(fastest['stops'])}\n")
                self.results_text.insert(tk.END, f"   Time: {fastest['total_time']} minutes\n")
                self.results_text.insert(tk.END, f"   Cost: ${fastest['total_cost']}\n\n")
            
            if cheapest:
                self.results_text.insert(tk.END, "💰 CHEAPEST ROUTE:\n")
                self.results_text.insert(tk.END, f"   {cheapest['route_name']}\n")
                self.results_text.insert(tk.END, f"   Stops: {' → '.join(cheapest['stops'])}\n")
                self.results_text.insert(tk.END, f"   Time: {cheapest['total_time']} minutes\n")
                self.results_text.insert(tk.END, f"   Cost: ${cheapest['total_cost']}\n")
        
        self.results_text.config(state='disabled')
    
    def open_google_maps(self):
        """Open Google Maps with directions for the selected route."""
        import webbrowser
        
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()
        
        if not start or not end:
            messagebox.showwarning("Warning", "Please select both starting location and destination first.")
            return
        
        if start == end:
            messagebox.showwarning("Warning", "Starting location and destination cannot be the same.")
            return
        
        # Create Google Maps URL for public transit directions
        start_encoded = start.replace(' ', '+')
        end_encoded = end.replace(' ', '+')
        
        # Add Cape Town context for better location accuracy
        maps_url = (f"https://www.google.com/maps/dir/{start_encoded},+Cape+Town,+South+Africa/"
                   f"{end_encoded},+Cape+Town,+South+Africa/@-33.9249,18.4241,12z/data=!3m1!4b1!4m2!4m1!3e3")
        
        try:
            webbrowser.open(maps_url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Google Maps: {e}")

def create_gui():
    """Create and run the GUI application."""
    root = tk.Tk()
    app = BusRouteApp(root)
    root.mainloop()
