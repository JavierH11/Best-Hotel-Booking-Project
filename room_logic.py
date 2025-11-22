from models import Room
from utils import validate_date
from storage import load_bookings
#Function that checks for room availability   
def is_room_available(room_id, check_in, check_out): #(WIP)
    #David Guzman 11/21/2025
    """Check if the room is available for any specific date that the user chooses

    Args:
        room_id (str): The individual unique id for a particular room
        check_in (str): The check-in date held in Year/Month/Day Fromat
        check_out (str): The check-out date that will be held in the Year/Month/Day Format

    Returns:
        bool: True if room is available and False if it isn't available
    """
    #Variable that holds the existing reservations
    bookings = load_bookings()
    #Variables that will hold dates for user check-in/out
    check_in_date = validate_date(check_in)
    check_out_date = validate_date(check_out)
    
    #Check each reservation for a conflict/double-booking etc
    for booking in bookings:
        #Skip if its a different room or reservation is cancelled
        if(booking.get('room_id') != room_id or booking.get('status') == 'CANCELLED'):
            continue
        #Variables that will hold the existing reservation dates that get checked
        booking_in = validate_date(booking['check_in'])
        booking_out = validate_date(booking['check_out'])
        
        #Check for a date overlap, room won't be available if there is an overlap
        if not (check_out_date <= booking_in or check_in_date >= booking_out):
            return False #Room was already taken basically
    
    return True #No issues, reservation confirmed

#Function to find those available rooms based on user choice
def get_available_rooms(rooms, check_in, check_out, num_guests, num_beds, amenities):
    #David Guzman 11/21/2025
    """Find available rooms based on user choice criteria such as number of guests, beds, date, and amenities

    Args:
        check_in (str): Check-in date variable in Year/Month/Day format
        check_out (str): Check-out date variable in Year/Month/Day format
        num_guests (int): Variable for number of guests chosen by user
        num_beds (int): Variable for number of beds chosen by the user
        amenities (list): The list of amenities the user chose, assuming they selected any

    Returns:
        list: GUI will show the user the list of available rooms based on their selections
    """
    #Array to hold available rooms if it passes thru the filters
    available = []  
    for room in rooms:
        #Filter for checking the guest capacity and bed capacity
        if room.max_guests < num_guests or room.num_beds < num_beds:
            continue
        #Filter for checking amenities selected, if any
        if amenities and not any(a in room.amenities for a in amenities):
            continue
        #Filter for checking if the room is available by calling on the 'is_room_available' method
        if is_room_available(room.room_id, check_in, check_out):
            available.append(room) #If we reach this point, it means the room passed through all filters and is available for user
    return available
