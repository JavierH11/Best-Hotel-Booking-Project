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
#from models import Room
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
    """

    print("testing testing")