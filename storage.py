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

from utils import load_bookings
import json
import os

