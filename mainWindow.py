"""
Hotel Booking System - Main Entry Point

This module serves as the entry point for the application. 
Run this file to start the Hotel Booking System.

Usage:
    python main.py

The main.py file initializes the tkinter window and starts the application event loop
"""

import tkinter as tk
from app import HotelBookingApp

def main():
    """
    Initialize and run the Hotel Booking Application

    Creates the main tkinter window and starts the application event loop.
    The evemt loop runs until the user closes the application window.

    Returns:
        None
    """
    # Create main tkinter window
    root = tk.Tk()

    # Initialize application
    app = HotelBookingApp(root)

    # Start event loop (blocks until window is closed)
    root.mainloop()

if __name__ == "__main__":
    main()