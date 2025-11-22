#```python
"""
Hotel Booking System - Data Models

This module defines the Room and Booking data structures used throughout
the hotel booking application.

Classes:
    Room: Represents a hotel room with amenities and pricing.
"""

class Room:
    """
    Represents a hotel room.
    
    A Room contains all necessary information about a hotel room including
    its type, capacity, number of beds, pricing, and available amenities.
    
    Attributes:
        room_id (str): Unique identifier for the room (e.g., "R001")
        room_type (str): Type of room (Single, Double, Suite)
        max_guests (int): Maximum number of guests allowed in room
        num_beds (int): Number of beds in the room
        price (float): Nightly rate in dollars
        amenities (list): List of available amenities (WiFi, AC, Bathtub, etc.)
    """
    
    def __init__(self, room_id, room_type, max_guests, num_beds, price, amenities):
        """
        Initialize a Room instance.
        
        Args:
            room_id (str): Unique room identifier
            room_type (str): Type of room (Single/Double/Suite)
            max_guests (int): Maximum guest capacity
            num_beds (int): Number of beds
            price (float): Nightly rate
            amenities (list): Available amenities
        """
        self.room_id = room_id
        self.room_type = room_type
        self.max_guests = max_guests
        self.num_beds = num_beds
        self.price = price
        self.amenities = amenities
#```
