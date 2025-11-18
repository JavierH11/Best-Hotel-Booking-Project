#```python
"""
Hotel Booking System - Utility Functions

This module contains helper functions for date validation, confirmation
number generation, and booking management.

Functions:
    validate_date: Validate date format (YYYY-MM-DD)
    generate_conf_number: Generate unique confirmation numbers
    load_bookings: Load bookings from JSON storage
    save_booking: Save new booking to JSON
    update_booking_status: Update existing booking status
    find_booking: Search for booking by confirmation number
"""

import json
import os
import random
import string
from datetime import datetime


def validate_date(date_string):
    """
    Validate if a string is a valid date in YYYY-MM-DD format.
    
    Attempts to parse the date string using standard format.
    Returns None if parsing fails.
    
    Args:
        date_string (str): Date string to validate
    
    Returns:
        datetime: Parsed datetime object if valid, None otherwise
    
    Example:
        >>> date = validate_date("2025-11-14")
        >>> print(type(date).__name__)
        datetime
        
        >>> date = validate_date("invalid")
        >>> print(date)
        None
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except:
        return None


def generate_conf_number():
    """
    Generate a random unique confirmation number.
    
    Creates a confirmation number in format "CONF-XXXXXXXX" where X
    is a random uppercase letter or digit. Used for all bookings.
    
    Returns:
        str: Confirmation number in format "CONF-XXXXXXXX"
    
    Example:
        >>> conf = generate_conf_number()
        >>> print(conf[:5])
        CONF-
        >>> print(len(conf))
        13
    """
    return 'CONF-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def load_bookings():
    """
    Load all bookings from the JSON storage file.
    
    Reads bookings.json file and returns all stored bookings.
    Returns empty list if file doesn't exist or on read error.
    
    Returns:
        list: List of booking dictionaries, empty list if none found
    
    Example:
        >>> bookings = load_bookings()
        >>> print(len(bookings))
        5
        >>> print(bookings[0]['confirmation_number'])
        CONF-ABC123XY
    """
    json_file = "bookings/bookings.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_booking(booking_dict):
    """
    Save a new booking to the JSON storage file.
    
    Appends new booking to existing bookings list and writes to disk.
    Creates bookings directory if it doesn't exist.
    
    Args:
        booking_dict (dict): Complete booking data dictionary
        
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        >>> booking = {
        ...     "confirmation_number": "CONF-ABC123",
        ...     "guest_name": "John Doe",
        ...     "total_price": 300.0
        ... }
        >>> success = save_booking(booking)
        >>> print(success)
        True
    """
    os.makedirs("bookings", exist_ok=True)
    bookings = load_bookings()
    bookings.append(booking_dict)
    try:
        with open("bookings/bookings.json", "w") as f:
            json.dump(bookings, f, indent=2)
        return True
    except:
        return False


def update_booking_status(conf_num, new_status):
    """
    Update the status of an existing booking.
    
    Finds booking by confirmation number and changes status to
    either CONFIRMED or CANCELLED. Then writes updated list back to disk.
    
    Args:
        conf_num (str): Confirmation number of booking to update
        new_status (str): New status (CONFIRMED or CANCELLED)
        
    Returns:
        bool: True if successful, False if booking not found
    
    Example:
        >>> updated = update_booking_status("CONF-ABC123", "CANCELLED")
        >>> print(updated)
        True
    """
    bookings = load_bookings()
    for booking in bookings:
        if booking.get('confirmation_number') == conf_num:
            booking['status'] = new_status
            try:
                with open("bookings/bookings.json", "w") as f:
                    json.dump(bookings, f, indent=2)
                return True
            except:
                return False
    return False


def find_booking(conf_num):
    """
    Find a booking by confirmation number.
    
    Searches through all bookings and returns the booking with matching
    confirmation number. Only returns non-cancelled bookings.
    
    Args:
        conf_num (str): Confirmation number to search for
        
    Returns:
        dict: Booking data if found, None otherwise
    
    Example:
        >>> booking = find_booking("CONF-ABC123")
        >>> if booking:
        ...     print(booking['guest_name'])
        John Doe
    """
    bookings = load_bookings()
    for booking in bookings:
        if (booking.get('confirmation_number') == conf_num and 
            booking.get('status') != 'CANCELLED'):
            return booking
    return None
#```