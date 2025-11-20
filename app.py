"""
Hotel Booking System - User Interface

This module contains the main HotelBookingApp class which handles all user interface 
screens and user interactions

Classes:
    HotelBookingApp: Main application controller
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta

# Import from other modules
from models import Room
#from utils import validate_date, generate_conf_number
#from storage import load_bookings, find_booking
#from createReservation_logic import create_reservation, modify_reservation, cancel_reservation
#from room_logic import get_available_rooms
#from email_service import send_email

class HotelBookingApp:
    """
    Main Hotel Booking Application

    This is the central controller that manages all user interface screens, user interactions,
    and coordinates between business logic and UI

    Attributes:
        root (tk.Tk): Main tkinter window
        rooms (list): List of available room objects
        admin_user (str): Admin username
        admin_pass (str): Admin password
        email_sender (str): Email address for notifications
        email_password (str): Email password fro SMTP
        current_frame (tk.frame): Currently displayed frame

    Example:
        >>> root = tk.Tk()
        >>> app = HotelBookingApp(root)
        >>> root.mainloop()
    """

    def __init__(self, root):
        """
        Initialize the Hotel Booking Application

        Sets up the main window, initializes room data, and displays the homepage

        Args: 
            root (tk.Tk): The main tkinter window
        """
        self.root = root
        self.root.title("Hotel Booking System")
        self.root.geometry("900x800")

        # Initialize room data - 3 room types available
        self.rooms = [
            Room("R001", "Single", 1, 1, 100.0, ["WiFi", "AC"]),
            Room("R002", "Double", 2, 1, 150.0, ["WiFi", "AC", "Bathtub"]),
            Room("R003", "Suite", 4, 2, 250.0, ["WiFi", "AC", "Bathtub", "Mini Bar"])
        ]

        # Admin credentials for report access
        self.admin_user = "admin"
        self.admin_pass = "admin123"

        # Email configuration - UPDATE THESE WITH YOUR EMAIL
        self.email_sender = "your_hotel_email@gmail.com"
        self.email_password = "your_app_password" # user Gmail app password

        # Track current frame for clearing
        self.current_frame = None

        # Show homepage
        self.show_homepage()

    def clear_screen(self):
        """
        Clear the current frame and prepare for new content.
        
        This method destroys the current frame to make room for the next screen.
        This is called at the beginning of every screen method.
        """
        if self.current_frame:
            self.current_frame.destroy()

    def show_homepage(self):
        """
        Display the main homepage with navigation buttons.
        
        Shows four main options:
        - Create New Reservation (Green)
        - Modify Reservation (Orange)
        - Cancel Reservation (Red)
        - Generate Admin Report (Purple)
        
        This is the first screen users see.
        """
        self.clear_screen()
        
        # Create main frame with light blue background
        frame = tk.Frame(self.root, bg="lightblue")
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        # Title
        tk.Label(frame, text="🏨 Hotel Booking System", 
                font=("Arial", 24, "bold"), bg="lightblue").pack(pady=30)
        tk.Label(frame, text="Welcome to Hotel Management", 
                font=("Arial", 12), bg="lightblue").pack(pady=10)

        # Create Reservation Button
        tk.Button(frame, text="✨ Create Reservation", 
                 font=("Arial", 12), bg="green", fg="white",
                 command=self.booking_step1, width=30, height=2).pack(pady=10)
        
        # Modify Reservation Button
        tk.Button(frame, text="📝 Modify Reservation", 
                 font=("Arial", 12), bg="orange", fg="white",
                 command=self.show_modify, width=30, height=2).pack(pady=10)
        
        # Cancel Reservation Button
        tk.Button(frame, text="❌ Cancel Reservation", 
                 font=("Arial", 12), bg="red", fg="white",
                 command=self.show_cancel, width=30, height=2).pack(pady=10)
        
        # Admin Report Button
        tk.Button(frame, text="📊 Admin Report", 
                 font=("Arial", 12), bg="purple", fg="white",
                 command=self.show_login, width=30, height=2).pack(pady=10)

    print("testing testing")