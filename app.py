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
from utils import validate_date, generate_conf_number
#from storage import load_bookings, find_booking
#from createReservation_logic import create_reservation, modify_reservation, cancel_reservation
from room_logic import get_available_rooms
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
        
    def booking_step1(self):
        """
        Display booking step 1: Guest preferences.

        Allows user to enter:
            - Check-in date
            - Check-out date
            - Number of guests
            - Number of beds
            - Preferred amenities
        
        User clicks "Search Rooms" to proceed to step 2
        """
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand= True, padx=20,pady=20)
        self.current_frame=frame

        # Title
        tk.Label(frame, text="Step 1: Your Preferences", font=("Arial",16,"bold")).pack(pady=10)

        # Check-In Date Input
        tk.Label(frame,teext="Check-In (YYYY-MM-DD):").pack()
        check_in_entry = tk.Entry(frame,width=20).pack()
        check_in_entry.insert(0, (datetime.now() + timedelta(day=2)).strftime("%Y-%m-%d"))

        # Check-Out Date Input
        tk.Label(frame, text="Check-Out (YYYY-MM-DD):",pady=10).pack()
        check_out_entry = tk.Entry(frame,width=20).pack()
        check_out_entry.insert(0, (datetime.now() + timedelta(day=2)).strftime("%Y-%m-%d"))

        # Number of guests dropdown menu
        tk.Label(frame, text="Guests:",pady=10).pack()
        guests_var = tk.StringVar(value="1")
        ttk.Combobox(frame, textvariable=guests_var, values=["1","2","3","4"],width=10,state="readonly").pack()

        # Number of beds dropdown menu
        tk.Label(frame, text="Beds:",pady=10).pack()
        beds_var = tk.StringVar(value="1")
        ttk.Combobox(frame, textvariable=guests_var, values=["1","2","3"],width=10,state="readonly").pack()

        # Amenities checkbox selection
        tk.Label(frame, text="Amenities:",pady=10).pack()
        amenity_check={}
        for amenity in ["Wifi","AC", "Bathtub", "Mini Bar"]:
            var = tk.BooleanVar()
            tk.Checkbutton(frame,text=amenity, variable=var).pack(anchor="w",padx=20)
            amenity_check[amenity] = var

        def search():
            "Handle Search Button - validate and proceed to step 2"
            # Get User Input
            check_in = check_in_entry.get()
            check_out = check_out_entry.get()

            # Validate Dates
            if not validate_date(check_in) or not validate_date(check_out):
                messagebox.showerror("ERROR", "Invalid date format. Use YYYY-MM-DD")
                return
            
            # Check that check-out is after check-in
            if validate_date(check_out) <= validate_date(check_in):
                messagebox.showerror("ERROR", "Check-out date must be after check-in date")
                return

            # Get Selected Amenities
            amenities = [a for a, v in amenity_check.items() if v.get()]

            # Get available rooms based on filters
            available = get_available_rooms(
                self.rooms, check_in, check_out,
                int(guests_var.get()), int(beds_var.get()), amenities
                )
            
            # Check if any rooms available
            if not available:
                messagebox.showerror(
                    "No Availability",
                    "No rooms match your criteria.\nTry different dates or preferences."
                    )
                return
            
            # Store preferences and proceed to step 2
            prefs={
                "check_in":check_in,
                "check_out":check_out,
                "nights": (validate_date(check_out) - validate_date(check_in)).days
            }
            self.booking_step2(available, prefs)

        # Buttons
        tk.Button(frame, text="Search Rooms", command=search, width=30,
                  height=2, bg="blue", fg="white", font=("Arial", 12)).pack(pady=15)
        tk.Button(frame, text="Back", command=self.show_homepage, width=30,
                  bg="gray", font=("Arial", 11)).pack()
    print("testing testing")