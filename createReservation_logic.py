"""
Best Hotel Booking - The reservation logic for the software

This module handles all business logic for creating, modifying, and canceling reservations. It will also work with the storage and email sections.

Functions:
    create_reservation: Create new reservation and send confirmation
    modify_reservation: Modify reservation and send notification
    cancel_reservation: Cancel reservation and send cancellation email
"""
#Files/methods from my teammates to make the program work
from utils import generate_conf_number
from storage import save_reservation, find_reservation, update_reservation_status
from email_service import send_email

#New reservation method/function when user selects that create new reservation button
def create_reservation(guest_info, room, preferences, sender_email, sender_password):
    """
    Create a new reservation and send confirmation email.
    
    Creates reservation record, saves to storage, and sends confirmation
    email to guest with reservation details.
    
    Args:
        guest_info (dict): Guest information dict with keys:
            - 'name': Full name
            - 'email': Email address
            - 'phone': Phone number
            - 'card': Credit card (for validation only)
        room (Room): Room object to book
        preferences (dict): reservation preferences with keys:
            - 'check_in': Check-in date "YYYY-MM-DD"
            - 'check_out': Check-out date "YYYY-MM-DD"
            - 'nights': Number of nights (int)
        sender_email (str): Hotel email address
        sender_password (str): Hotel email app password
        
    Returns:
        dict: Created reservation data including confirmation number
        
    Example:
        >>> guest = {
        ...     "name": "John Doe",
        ...     "email": "john@email.com",
        ...     "phone": "555-1234",
        ...     "card": "4111111111111111"
        ... }
        >>> from models import Room
        >>> room = Room("R001", "Single", 1, 1, 100.0, ["WiFi"])
        >>> prefs = {"check_in": "2025-11-20", "check_out": "2025-11-22", "nights": 2}
        >>> reservation = create_reservation(guest, room, prefs, "hotel@gmail.com", "apppass")
        >>> print(reservation['confirmation_number'])
        CONF-ABC123XY
    """
    #This will generate a unique confirmation number for each user that creates a reservation
    conf_num = generate_conf_number()
    #This will calculate the total price for the reservation
    total_price = preferences['nights'] * room.price
    #This will create a dictionary for the reservation with the details specifying that particular reservation....
    reservation = {
        "confirmation_number": conf_num,
        "room_id": room.room_id,
        "guest_name": guest_info['name'],
        "guest_email": guest_info['email'],
        "guest_phone": guest_info['phone'],
        "room_type": room.room_type,
        "check_in": preferences['check_in'],
        "check_out": preferences['check_out'],
        "nights": preferences['nights'],
        "total_price": total_price,
        "status": "CONFIRMED"
    }
    #This will save the reservation reservation info to the storage
    save_reservation(reservation)
    #The body of the email that the user is gonna receive; How the confirmation email looks basically
    email_subject = "Reservation Confirmation - Best Hotel Booking"
    email_body = f"""Dear {guest_info['name']},

Your reservation has been confirmed!

Confirmation Number: {conf_num}
Room Type: {room.room_type}
Check-in: {preferences['check_in']}
Check-out: {preferences['check_out']}
Number of Nights: {preferences['nights']}
Nightly Rate: ${room.price}
Total Price: ${total_price:.2f}

Room Amenities: {', '.join(room.amenities)}

Thank you for reservation with us!

Best regards,
Best Hotel Booking"""
    #This will send out a confirmation email to the user that their reservation was made along with the unique confirmation #
    send_email(sender_email, sender_password, guest_info['email'], 
               email_subject, email_body)
    return reservation
#The method/function that makes the reservation changes that the user inputs.
def modify_reservation(old_conf_num, new_guest_info, new_preferences, 
                   room, sender_email, sender_password):
    """
    Modify an existing reservation and send notification email to the user. It also cancels the old reservation, creates new reservation with updated details, 
    and sends email to guest that the reservation has been modified.
    
    Args:
        old_conf_num (str): Confirmation number of reservation to modify
        new_guest_info (dict): Updated guest information
        new_preferences (dict): New reservation preferences
        room (Room): Room object
        sender_email (str): Hotel email address
        sender_password (str): Hotel email app password
        
    Returns:
        dict: New reservation data, or None if old reservation not found
    
    Example:
        >>> # Modify existing reservation
        >>> new_prefs = {"check_in": "2025-11-22", "check_out": "2025-11-25", "nights": 3}
        >>> new_guest = {"name": "John Doe", "email": "john@email.com", ...}
        >>> reservation = modify_reservation("CONF-OLD123", new_guest, new_prefs, room, email, pass)
        >>> if reservation:
        ...     print(f"New confirmation: {reservation['confirmation_number']}")
    """
    #This will find an old reservation if it exists. If it doesn't exist it'll just return NOne.
    old_reservation = find_reservation(old_conf_num)
    if not old_reservation:
        print(f"ERROR: Old reservation {old_conf_num} not found")
        return None
    #This will update the status of that old reservation to 'Cancelled'
    update_reservation_status(old_conf_num, "CANCELLED")
    #This will generate a new confirmation number on that reservation for the user.
    new_conf_num = generate_conf_number()
    #This will calculate the new total price, (hopefully they paid more than before)
    new_total_price = new_preferences['nights'] * room.price
    #This will create that new reservation with whatever additions/subtractions the user selected.
    new_reservation = {
        "confirmation_number": new_conf_num,
        "room_id": room.room_id,
        "guest_name": new_guest_info['name'],
        "guest_email": new_guest_info['email'],
        "guest_phone": new_guest_info['phone'],
        "room_type": room.room_type,
        "check_in": new_preferences['check_in'],
        "check_out": new_preferences['check_out'],
        "nights": new_preferences['nights'],
        "total_price": new_total_price,
        "status": "CONFIRMED"
    }
    
    #This will then save that new reservation to the record for the report
    save_reservation(new_reservation)
    #The body of the email for that modified confirmation request from the user.
    email_subject = "Reservation Modified - Best Hotel Booking"
    email_body = f"""Dear {new_guest_info['name']},

Your reservation has been successfully modified!

Previous Confirmation Number: {old_conf_num}
New Confirmation Number: {new_conf_num}

Updated reservation Details:
Check-in: {new_preferences['check_in']}
Check-out: {new_preferences['check_out']}
Number of Nights: {new_preferences['nights']}
Total Price: ${new_total_price:.2f}

The previous reservation has been cancelled.

Thank you for reservation with us!

Best regards,
Best Hotel Booking"""
    #This will lastly send out an email to the user for that modified reservation
    send_email(sender_email, sender_password, new_guest_info['email'],
               email_subject, email_body)
    return new_reservation
#The unfortunate method/function to cancel a reservation, maybe we should remove it so we don't lose money tho the user might sue us.                       
def cancel_reservation(conf_num, reservation, sender_email, sender_password):
    """
    Cancel an existing reservation and send notification email.
    
    Updates reservation status to 'Cancelled' and sends cancellation confirmation email to guest.
    
    Args:
        conf_num (str): Confirmation number to cancel
        reservation (dict): reservation data
        sender_email (str): Hotel email address
        sender_password (str): Hotel email app password
        
    Returns:
        bool: True if successful, False if update failed
    
    Example:
        >>> reservation = find_reservation("CONF-ABC123")
        >>> success = cancel_reservation("CONF-ABC123", reservation, email, pass)
        >>> print(success)
        True
    """
    #Update the status of a reservation to 'Cancelled', user is too good for us apparently
    success = update_reservation_status(conf_num, "CANCELLED")
    if success:
        #Generate cancellation confirmation number for user
        cancel_conf_num = f"CANCEL-{generate_conf_number()}"
        email_subject = "reservation Cancelled - Best Hotel Booking"
        email_body = f"""Dear {reservation['guest_name']},

Your reservation has been cancelled. We apologize for not being good enough for you!

Original Confirmation Number: {conf_num}
Cancellation Confirmation Number: {cancel_conf_num}

Cancelled reservation Details:
Room: {reservation['room_type']}
Check-in: {reservation['check_in']}
Check-out: {reservation['check_out']}
Original Total: ${reservation['total_price']}

Thank you for your understanding. We hope to see you again!

Best regards,
Best Hotel Booking"""
        #Send cancellation email to the user, we didn't want them anyway...
        send_email(sender_email, sender_password, reservation['guest_email'],
                   email_subject, email_body)
    return success
