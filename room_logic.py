"""
Hotel Booking System - Room Business Logic

This module handles room availability checking, filtering, and searching.

Functions:
    is_room_available: Check if room is available for dates
    get_available_rooms: Get list of available rooms matching criteria
"""

from utils import validate_date
from storage import load_bookings


def is_room_available(room_id, check_in, check_out):
    """
    Check if a specific room is available for the given date range.
    
    Loads all bookings and checks for date interesection (If a date is already taken). A room will not be
    available if another 'confirmed' booking overlaps with requested dates. Note that cancelled bookings do not block availability.
    
    Args:
        room_id (str): Room ID to check (e.g., "R001")
        check_in (str): Check-in date in format "YYYY-MM-DD"
        check_out (str): Check-out date in format "YYYY-MM-DD"
        
    Returns:
        bool: True if available, False if booked
    
    Example:
        >>> available = is_room_available("R001", "2025-11-20", "2025-11-22")
        >>> print(available)
        True
        
        >>> available = is_room_available("R001", "2025-11-21", "2025-11-23")
        >>> print(available)
        False  # If already booked for 11-21 to 11-23
    """
    #Load all existing bookings
    bookings = load_bookings()
    
    #Parse through the requested dates
    check_in_date = validate_date(check_in)
    check_out_date = validate_date(check_out)
    
    #Check each booking for any intersection
    for booking in bookings:
        #Skip if different room or booking is cancelled
        if booking.get('room_id') != room_id or booking.get('status') == 'CANCELLED':
            continue
        
        #Parse the existing booking dates
        booking_check_in = validate_date(booking['check_in'])
        booking_check_out = validate_date(booking['check_out'])
        
        #Check for a date overlap
        #Room will 'Not' available if dates overlap
        if not (check_out_date <= booking_check_in or check_in_date >= booking_check_out):
            return False  #Room is booked during this period
    
    #If there were no issues, booking is confirmed
    return True


def get_available_rooms(rooms, check_in, check_out, num_guests, num_beds, amenities):
    """
    Get list of available rooms matching all of the filter criteria
    
    Filters rooms by:
    1. Guest capacity (max_guests >= num_guests)
    2. Bed count (num_beds >= required)
    3. Amenities (has all requested amenities)
    4. Date availability (not booked during dates)
    
    Args:
        rooms (list): List of Room objects to filter
        check_in (str): Check-in date "YYYY-MM-DD"
        check_out (str): Check-out date "YYYY-MM-DD"
        num_guests (int): Number of guests
        num_beds (int): Minimum beds required
        amenities (list): Required amenities (empty list = any amenities OK)
        
    Returns:
        list: Filtered list of available Room objects
    
    Example:
        >>> from models import Room
        >>> rooms = [
        ...     Room("R001", "Single", 1, 1, 100.0, ["WiFi", "AC"]),
        ...     Room("R002", "Double", 2, 1, 150.0, ["WiFi", "AC", "Bathtub"])
        ... ]
        >>> available = get_available_rooms(
        ...     rooms, "2025-11-20", "2025-11-22", 2, 1, ["WiFi"]
        ... )
        >>> print(len(available))
        2
    """
    available = []
    
    for room in rooms:
        #First filter will check the guest capacity
        if room.max_guests < num_guests:
            continue  # Room doesn't fit enough guests
        
        #Second filter will check the bed count
        if room.num_beds < num_beds:
            continue  # Room doesn't have enough beds
        
        #Third filter will check for any amenities (if the customer requested any)
        if amenities:  #Only check if amenities list is not empty
            #Room must have 'All' requested amenities
            has_all_amenities = all(a in room.amenities for a in amenities)
            if not has_all_amenities:
                continue  #This means that a room is missing required amenity
        
        #Fourth Filter will check for date availability
        if not is_room_available(room.room_id, check_in, check_out):
            continue  #This means that a room is already booked for these dates
        
        #This means that a room passed through all the filters and is available for the user to select
        available.append(room)
    
    return available
