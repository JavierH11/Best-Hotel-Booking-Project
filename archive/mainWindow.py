"""
Hotel Reservation Software - Main Loop

This is the main file for the program. 
User must launch this file to use Hotel Reservation Software.

In terminal enter:
    python main.py

This file initializes the main loop for the program
"""

import tkinter as tk
from app import HotelBookingApp

def main():
    """
    Starts the program from here by calling mainloop().
    The main loops keeps going until user closes the program/window.

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