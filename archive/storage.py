from utils import load_bookings

"""
Hotel Booking System - Data Storage

This module handles all file I/O operations for persisting booking data
to a JSON file. All bookings are stored in bookings/bookings.json

Functions:
    load_bookings: Load all bookings from JSON file
    save_booking: Add new booking to JSON file
    update_booking_status: Update existing booking status
    find_booking: Search for booking by confirmation number
"""

import json
import os


def load_bookings():
    """
    Load all bookings from the JSON storage file.
    
    Attempts to read bookings/bookings.json and parse as JSON.
    Returns empty list if file doesn't exist or JSON is invalid.
    
    Returns:
        list: List of booking dictionaries
        
    Example:
        >>> bookings = load_bookings()
        >>> print(f"Total bookings: {len(bookings)}")
        Total bookings: 5
    """
    json_file = "bookings/bookings.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading bookings: {e}")
            return []
    return []


def save_booking(booking_dict):
    """
    Save a new booking to the JSON storage file.
    
    Creates bookings directory if needed, loads existing bookings,
    appends new one, and writes back to disk.
    
    Args:
        booking_dict (dict): Complete booking data to save
        
    Returns:
        bool: True if saved successfully, False on error
    
    Example:
        >>> booking = {
        ...     "confirmation_number": "CONF-XYZ789",
        ...     "guest_name": "Jane Smith",
        ...     "total_price": 450.50
        ... }
        >>> success = save_booking(booking)
        >>> print(success)
        True
    """
    # Create directory if it doesn't exist
    os.makedirs("bookings", exist_ok=True)
    
    # Load existing bookings
    bookings = load_bookings()
    
    # Append new booking
    bookings.append(booking_dict)
    
    # Write to file
    try:
        with open("bookings/bookings.json", "w") as f:
            json.dump(bookings, f, indent=2)
        print(f"Booking saved: {booking_dict['confirmation_number']}")
        return True
    except Exception as e:
        print(f"Error saving booking: {e}")
        return False


def update_booking_status(conf_num, new_status):
    """
    Update the status of an existing booking.
    
    Finds booking by confirmation number and changes its status
    to either CONFIRMED or CANCELLED.
    
    Args:
        conf_num (str): Confirmation number of booking to update
        new_status (str): New status ("CONFIRMED" or "CANCELLED")
        
    Returns:
        bool: True if updated successfully, False if not found
    
    Example:
        >>> success = update_booking_status("CONF-ABC123", "CANCELLED")
        >>> print(success)
        True
    """
    bookings = load_bookings()
    
    # Find and update booking
    for booking in bookings:
        if booking.get('confirmation_number') == conf_num:
            booking['status'] = new_status
            try:
                with open("bookings/bookings.json", "w") as f:
                    json.dump(bookings, f, indent=2)
                print(f"Booking {conf_num} updated to {new_status}")
                return True
            except Exception as e:
                print(f"Error updating booking: {e}")
                return False
    
    print(f"Booking {conf_num} not found")
    return False



def find_booking(conf_num):
    """
    Find a booking by confirmation number.
    
    Searches through all bookings for matching confirmation number.
    Only returns bookings with CONFIRMED status (excludes CANCELLED).
    
    Args:
        conf_num (str): Confirmation number to search for
        
    Returns:
        dict: Booking data if found, None if not found
    
    Example:
        >>> booking = find_booking("CONF-ABC123")
        >>> if booking:
        ...     print(f"Guest: {booking['guest_name']}")
        Guest: John Doe
    """
    bookings = load_bookings()
    
    for booking in bookings:
        # Check if confirmation number matches and booking is not cancelled
        if (booking.get('confirmation_number') == conf_num and 
            booking.get('status') != 'CANCELLED'):
            return booking
    
    # Not found
    return None