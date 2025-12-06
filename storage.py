from utils import load_bookings

"""
Hotel Booking System - Data Storage

This module handles all file I/O operations for persisting booking data to a JSON file. All bookings are stored in bookings/bookings.json

Functions:
    load_bookings: Load all bookings from JSON file
    save_booking: Add new booking to JSON file
    update_booking_status: Update existing booking status
    find_booking: Search for booking by confirmation number
Note: There is alot of overlap between storage.py and models.py, next stages Sergio and Javier will have to work together to merge both files or find another solution
"""

import json
import os


def load_bookings():
    #Javier Herrera 11/21/2025
    """
    Load all bookings from the JSON storage file.
    
    Reads bookings.json file and returns all stored bookings.
    Returns empty list if file doesn't exist or on read error.
    
    Returns:
        list: List of booking dictionaries, empty list if none found
    """
    json_file = "bookings/bookings.json"    # Set the path to the JSON file that stores bookings
    if os.path.exists(json_file):           # Check if the bookings JSON file actually exists on disk
        try:                                # Start a try block to safely attempt to read and parse the JSON file
            with open(json_file, "r") as f: # Open the bookings file in read mode and assign it to f
                return json.load(f)         # Parse the JSON content into Python objects and return the list of bookings
        except:                             # If any error occurs while opening or reading/parsing the file
            return []                       # Fail gracefully by returning an empty list instead of crashing
    return []                               # If the file does not exist at all, return an empty list as there are no bookings


def save_booking(booking_dict):
    #Sergio Ruelas 11/21/2025
    """Save a new booking to JSON file"""
    os.makedirs("bookings", exist_ok=True)          # Ensure the 'bookings' directory exists, create it if it does not
    bookings = load_bookings()                      # Load the current list of bookings from the JSON file (or [] if none)
    bookings.append(booking_dict)                   # Add the new booking dictionary to the in‑memory bookings list
    with open("bookings/bookings.json", "w") as f:  # Open the bookings JSON file in write mode (overwrite existing)
        json.dump(bookings, f, indent=2)            # Serialize the full bookings list to JSON and write it with pretty indentation

'''
# Test ID: STOR 1 (starts)
# Tests the data to ensure save functinality
test_booking = {
    "confirmation_number": "#TEST123",
    "guest_name": "Test User",
    "guest_email": "test@example.com",
    "guest_phone": "555-1234",
    "room_type": "Double",
    "room_id": "R002",
    "check_in": "2025-12-10",
    "check_out": "2025-12-12",
    "nights": 2,
    "total_price": 300.0,
    "status": "CONFIRMED"
}

# Execute the save
save_booking(test_booking)

# Check what was created
print("✅ STOR_001 TEST EXECUTION")
print("=" * 50)

# Read back the file
with open("bookings/bookings.json", "r") as f:
    saved_data = json.load(f)

print(f"Number of bookings saved: {len(saved_data)}")
print(f"Booking confirmation number: {saved_data[0]['confirmation_number']}")
print(f"Booking status: {saved_data[0]['status']}")
print("=" * 50)

## Test ID: STOR 1 (ends)

# Test ID: STOR 2 (starts)
# Clear old data
if os.path.exists("bookings"):
    import shutil
    shutil.rmtree("bookings")

booking1 = {
    "confirmation_number": "#ABC001",
    "guest_name": "John Doe",
    "guest_email": "john@example.com",
    "guest_phone": "555-1111",
    "room_type": "Single",
    "room_id": "R001",
    "check_in": "2025-12-10",
    "check_out": "2025-12-12",
    "nights": 2,
    "total_price": 200.0,
    "status": "CONFIRMED"
}

booking2 = {
    "confirmation_number": "#ABC002",
    "guest_name": "Jane Doe",
    "guest_email": "jane@example.com",
    "guest_phone": "555-2222",
    "room_type": "Double",
    "room_id": "R002",
    "check_in": "2025-12-15",
    "check_out": "2025-12-17",
    "nights": 2,
    "total_price": 300.0,
    "status": "CONFIRMED"
}

booking3 = {
    "confirmation_number": "#ABC003",
    "guest_name": "Bob Smith",
    "guest_email": "bob@example.com",
    "guest_phone": "555-3333",
    "room_type": "Suite",
    "room_id": "R003",
    "check_in": "2025-12-20",
    "check_out": "2025-12-22",
    "nights": 2,
    "total_price": 500.0,
    "status": "CONFIRMED"
}

# SAVE THREE BOOKINGS (one after another)
print("✅ STOR_002 TEST EXECUTION")
print("=" * 50)

print("Saving booking 1...")
save_booking(booking1)

print("Saving booking 2...")
save_booking(booking2)

print("Saving booking 3...")
save_booking(booking3)

# READ BACK AND VERIFY
with open("bookings/bookings.json", "r") as f:
    all_bookings = json.load(f)

print(f"\nTotal bookings saved: {len(all_bookings)}")
print(f"Booking 1: {all_bookings[0]['confirmation_number']} - {all_bookings[0]['guest_name']}")
print(f"Booking 2: {all_bookings[1]['confirmation_number']} - {all_bookings[1]['guest_name']}")
print(f"Booking 3: {all_bookings[2]['confirmation_number']} - {all_bookings[2]['guest_name']}")
print("=" * 50)

# Test ID: STOR 2 (ends)
'''

def update_booking_status(conf_num, new_status):
    #Javier Herrera 11/21/2025
    """Update booking status in JSON file"""
    bookings = load_bookings()
    for booking in bookings:
        if booking.get('confirmation_number') == conf_num:
            booking['status'] = new_status
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
