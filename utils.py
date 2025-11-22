#```python
"""
Hotel Booking System - Utility Functions

This module contains helper functions for date validation, confirmation
number generation, and booking management.

Functions:
    save_booking: Save new booking to JSON
    update_booking_status: Update existing booking status
    find_booking: Search for booking by confirmation number
    validate_date: Validate date format (YYYY-MM-DD)
    generate_conf_number: Generate unique confirmation numbers
    load_bookings: Load bookings from JSON storage
"""

import json
import os
import random
import string
from datetime import datetime

def load_bookings():
    #Javier Herrera 11/21/2025
    """
    Load all bookings from the JSON storage file.
    
    Reads bookings.json file and returns all stored bookings.
    Returns empty list if file doesn't exist or on read error.
    
    Returns:
        list: List of booking dictionaries, empty list if none found
    """
    json_file = "bookings/bookings.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def update_booking_status(conf_num, new_status):
    #Javier Herrera 11/21/2025
    """Update booking status in JSON file"""
    bookings = load_bookings()
    for booking in bookings:
        if booking.get('confirmation_number') == conf_num:
            booking['status'] = new_status
    with open("bookings/bookings.json", "w") as f:
        json.dump(bookings, f, indent=2)

        def validate_date(date_string):
    #Sergio Ruelas 11/21/2025
    """
    Validate if a string is a valid date in YYYY-MM-DD format.
    
    Attempts to parse the date string using standard format.
    Returns None if parsing fails.
    
    Args:
        date_string (str): Date string to validate
    
    Returns:
        datetime: Parsed datetime object if valid, None otherwise
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except:
        return None

def generate_conf_number():
    #Sergio Ruelas 11/21/2025
    """
    Generate a random unique confirmation number.
    
    Creates a confirmation number in format "CONF-XXXXXXXX" where X
    is a random uppercase letter or digit. Used for all bookings.
    
    Returns:
        str: Confirmation number in format "CONF-XXXXXXXX"
    """
    return '#' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def save_booking(booking_dict):
    #Sergio Ruelas 11/21/2025
    """Save a new booking to JSON file"""
    os.makedirs("bookings", exist_ok=True)
    bookings = load_bookings()
    bookings.append(booking_dict)
    with open("bookings/bookings.json", "w") as f:
        json.dump(bookings, f, indent=2)

def find_booking(conf_num):
    #Sergio Ruelas 11/21/2025  
    """Find a particular reservation by inputting a confirmation number
    
    Args:
        conf_num (str): The confirmation number
        
    Returns:
        dict: Reservation with all the details particular to that confirmation number
    """
    bookings = load_bookings()
    for booking in bookings:
        if (booking.get('confirmation_number') == conf_num and booking.get('status') != 'CANCELLED'):
            return booking
    return None
#```