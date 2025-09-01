# Week 7 Project: Bus Route Comparator
# This program compares different bus routes to find the fastest and cheapest options.
# Main entry point for the application

from tkinter import messagebox
from gui import create_gui

def main():
    """Main function to start the application."""
    try:
        create_gui()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
