import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import os
import json
import random
import string
import smtplib
from app import BestHotelBookingGroup
from models import Room
#from createReservation_logic import create_reservation, modify_reservation, cancel_reservation
#from room_logic import is_room_available, get_available_rooms
#from utils import validate_date , generate_conf_number, load_bookings, save_booking, update_booking_status, find_booking
#from email_service import send_email #EMAIL IS A WIP, DOESNT REALLY WORK 
#from storage import load_bookings, save_booking, update_booking_status, find_booking
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#from models.py  got all the functions moved for file manipulation. It needs to be updated

#Room Data.py is keeping class Room 
'''
class Room:
    """Represents a hotel room"""
    def __init__(self, room_id, room_type, max_guests, num_beds, price, amenities):
        self.room_id = room_id
        self.room_type = room_type
        self.max_guests = max_guests
        self.num_beds = num_beds
        self.price = price
        self.amenities = amenities

#from utils

#Utility methods

def validate_date(date_string):
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

def save_booking(booking_dict):
    #Sergio Ruelas 11/21/2025
    """Save a new booking to JSON file"""
    os.makedirs("bookings", exist_ok=True)
    bookings = load_bookings()
    bookings.append(booking_dict)
    with open("bookings/bookings.json", "w") as f:
        json.dump(bookings, f, indent=2)

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
        dist: Reservation with all the details particular to that confirmation number
    """
    bookings = load_bookings()
    for booking in bookings:
        if booking.get('confirmation_number') == conf_num and booking.get('status') != 'CANCELLED':
            return booking
    return None

def generate_conf_number():
    #Sergio Ruelas 11/21/2025
    """Generate random confirmation number for user

    Returns:
        str: Confirmation number for reservation to be displayed to user at the end
    """
    return '#' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ============ MAIN APPLICATION ============

class BestHotelBookingGroup:

    def __init__(self, root):
        self.root = root
        self.root.title("Best Hotel Booking Group")
        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Room data
        self.rooms = [
            Room("R001", "Single", 1, 1, 100.0, ["WiFi", "AC"]),
            Room("R002", "Double", 2, 1, 150.0, ["WiFi", "AC", "Bathtub"]),
            Room("R003", "Suite", 4, 2, 250.0, ["WiFi", "AC", "Bathtub", "Mini-Bar"])
        ]
        
        # Admin credentials
        self.admin_user = "admin"
        self.admin_pass = "admin123"
        
        # Email settings - UPDATE THESE
        self.email_sender = "your_hotel_email@gmail.com"
        self.email_password = "your_app_password"
        
        self.current_frame = None
        self.show_homepage()

    def clear_screen(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()

    def send_email(self, recipient, subject, message):
        """Send email to guest"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.email_sender, self.email_password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Email failed: {e}")

    #Function that checks for room availability   
    def is_room_available(self, room_id, check_in, check_out): #(WIP)
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
    def get_available_rooms(self, check_in, check_out, num_guests, num_beds, amenities):
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
        for room in self.rooms:
            #Filter for checking the guest capacity and bed capacity
            if room.max_guests < num_guests or room.num_beds < num_beds:
                continue
            #Filter for checking amenities selected, if any
            if amenities and not any(a in room.amenities for a in amenities):
                continue
            #Filter for checking if the room is available by calling on the 'is_room_available' method
            if self.is_room_available(room.room_id, check_in, check_out):
                available.append(room) #If we reach this point, it means the room passed through all filters and is available for user
        return available

# from app

    #Gui Screen Section

    def show_homepage(self):
        #Matthew Cabrera 11/21/2025
        """The main menu screen display for the GUI"""
        self.clear_screen()
        frame = tk.Frame(self.root, bg="lightblue")
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        tk.Label(frame, text="Best Hotel Booking Group", font=("Times New Roman", 24, "bold"), 
                 bg="lightblue").pack(pady=30)
        tk.Label(frame, text="Welcome, Esteemed Guest To The Greatest Hotel in The History of The Universe Itself!", font=("Times New Roman", 16), 
                 bg="lightblue").pack(pady=10)
        tk.Button(frame, text="Create Reservation", font=("Times New Roman", 12), bg="green", 
                  fg="white", command=self.preferences, width=30, height=2).pack(pady=10)
        tk.Button(frame, text="Modify Reservation", font=("Times New Roman", 12), bg="orange", 
                  fg="white", command=self.show_modify, width=30, height=2).pack(pady=10)
        tk.Button(frame, text="Cancel Reservation", font=("Times New Roman", 12), bg="red", 
                  fg="white", command=self.show_cancel, width=30, height=2).pack(pady=10)
        tk.Button(frame, text="Admin Report", font=("Times New Roman", 12), bg="purple", 
                  fg="white", command=self.show_login, width=30, height=2).pack(pady=10)

    # ============ BOOKING FLOW (3 STEPS) ============

    def preferences(self):
        """Step 1: Enter preferences"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame
        tk.Label(frame, text="Select your preferences", font=("Times New Roman", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="Check-in (YYYY-MM-DD):").pack()
        check_in_entry = tk.Entry(frame, width=20)
        check_in_entry.pack()
        check_in_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        tk.Label(frame, text="Check-out (YYYY-MM-DD):", pady=10).pack()
        check_out_entry = tk.Entry(frame, width=20)
        check_out_entry.pack()
        check_out_entry.insert(0, (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"))
        tk.Label(frame, text="Guests:", pady=10).pack()
        guests_var = tk.StringVar(value="1")
        ttk.Combobox(frame, textvariable=guests_var, values=["1", "2", "3", "4"], 
                     width=10, state="readonly").pack()
        tk.Label(frame, text="Beds:", pady=10).pack()
        beds_var = tk.StringVar(value="1")
        ttk.Combobox(frame, textvariable=beds_var, values=["1", "2", "3"], 
                     width=10, state="readonly").pack()

        tk.Label(frame, text="Amenities:", pady=10).pack()
        amenity_checks = {}
        for amenity in ["WiFi", "AC", "Bathtub", "Mini Bar"]:
            var = tk.BooleanVar()
            tk.Checkbutton(frame, text=amenity, variable=var).pack(anchor="w", padx=20)
            amenity_checks[amenity] = var

        def search():
            """Prepares a display GUI for room availability based on the user's selections"""
            check_in = check_in_entry.get()
            check_out = check_out_entry.get()
            
            if not validate_date(check_in) or not validate_date(check_out):
                messagebox.showerror("Error", "Invalid date format")
                return
            
            if validate_date(check_out) <= validate_date(check_in):
                messagebox.showerror("Error", "Check-out must be after check-in")
                return
            
            amenities = [a for a, v in amenity_checks.items() if v.get()]
            available = self.get_available_rooms(check_in, check_out, 
                                                 int(guests_var.get()), 
                                                 int(beds_var.get()), 
                                                 amenities)
            
            if not available:
                messagebox.showerror("No Availability", "No rooms match your criteria")
                return
            
            prefs = {
                "check_in": check_in,
                "check_out": check_out,
                "nights": (validate_date(check_out) - validate_date(check_in)).days
            }
            self.room_GUI(available, prefs)

        tk.Button(frame, text="Search Rooms", width=30, height=2, 
                  bg="blue", fg="white", command=search).pack(pady=15)
        tk.Button(frame, text="Back", width=30, bg="gray", 
                  command=self.show_homepage).pack()

    def room_GUI(self, available_rooms, prefs):
        """Step 2: Select room"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame
        tk.Label(frame, text="Select a Room!", font=("Times New Roman", 16, "bold")).pack(pady=10)
        tk.Label(frame, text=f"{prefs['check_in']} to {prefs['check_out']} "
                 f"({prefs['nights']} nights)", 
                 bg="lightyellow", padx=10, pady=5).pack(fill="x", pady=10)
        room_var = tk.StringVar()
        room_frame = tk.Frame(frame, bg="lightgray", relief="sunken", bd=1)
        room_frame.pack(fill="both", expand=True, padx=10, pady=10)
        canvas = tk.Canvas(room_frame, bg="lightgray")
        scrollbar = ttk.Scrollbar(room_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="lightgray")
        scroll_frame.bind("<Configure>", 
                         lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for room in available_rooms:
            total = prefs['nights'] * room.price
            amenity_str = ", ".join(room.amenities)
            
            room_box = tk.Frame(scroll_frame, bg="white", relief="ridge", bd=2)
            room_box.pack(fill="x", padx=5, pady=5)
            
            tk.Radiobutton(room_box, text=f"{room.room_type} - ${room.price}/night",
                          variable=room_var, value=room.room_id,
                          font=("Times New Roman", 11), bg="white").pack(anchor="w", padx=10, pady=5)
            tk.Label(room_box, text=f"Beds: {room.num_beds} | Amenities: {amenity_str}\n"
                    f"Total: ${total:.2f}",
                    font=("Times New Roman", 9), bg="white", fg="darkblue").pack(anchor="w", padx=30)

        def next_step():
            if not room_var.get():
                messagebox.showerror("Error", "Select a room")
                return
            
            room = next((r for r in available_rooms if r.room_id == room_var.get()), None)
            self.guest_Details({
                "prefs": prefs,
                "room": room,
                "total": prefs['nights'] * room.price})

        tk.Button(frame, text="Continue", width=30, height=2, 
                  bg="green", fg="white", command=next_step).pack(pady=10)
        tk.Button(frame, text="Back", width=30, bg="gray",
                  command=self.preferences).pack()

    def guest_Details(self, booking_info):
        """Step 3: Enter guest details"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame
        tk.Label(frame, text="Please enter your information!", font=("Times New Roman", 16, "bold")).pack(pady=10)
        #Summary
        summary_frame = tk.LabelFrame(frame, text="Summary", padx=10, pady=10, bg="lightblue")
        summary_frame.pack(fill="x", pady=10)
        room = booking_info["room"]
        prefs = booking_info["prefs"]
        summary_text = (f"Room: {room.room_type} | Check-in: {prefs['check_in']}\n"
                       f"Check-out: {prefs['check_out']} | Total: ${booking_info['total']:.2f}")
        tk.Label(summary_frame, text=summary_text, bg="lightblue").pack(anchor="w")

        #Guest info
        tk.Label(frame, text="Name:", pady=10).pack()
        name_entry = tk.Entry(frame, width=30)
        name_entry.pack()
        tk.Label(frame, text="Email:", pady=10).pack()
        email_entry = tk.Entry(frame, width=30)
        email_entry.pack()
        tk.Label(frame, text="Phone:", pady=10).pack()
        phone_entry = tk.Entry(frame, width=20)
        phone_entry.pack()
        tk.Label(frame, text="Card Number:", pady=10).pack()
        card_entry = tk.Entry(frame, width=20)
        card_entry.pack()

        def confirm():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            card = card_entry.get()

            if not all([name, email, phone, card]):
                messagebox.showerror("Error", "Fill all fields")
                return

            conf_num = generate_conf_number()
            booking = {
                "confirmation_number": conf_num,
                "room_id": room.room_id,
                "guest_name": name,
                "guest_email": email,
                "guest_phone": phone,
                "room_type": room.room_type,
                "check_in": prefs['check_in'],
                "check_out": prefs['check_out'],
                "nights": prefs['nights'],
                "total_price": booking_info['total'],
                "status": "CONFIRMED"
            }
            save_booking(booking)

            # Send email (WIP, doesn't work yet)
            email_msg = (f"Dear {name},\n\nBooking confirmed!\n"
                        f"Confirmation: {conf_num}\nRoom: {room.room_type}\n"
                        f"Check-in: {prefs['check_in']}\nCheck-out: {prefs['check_out']}\n"
                        f"Total: ${booking_info['total']:.2f}\n\nThank you!")
            self.send_email(email, "Booking Confirmation", email_msg)
            self.show_confirmation(conf_num, name, email, phone, prefs, room, booking_info['total'])

        tk.Button(frame, text="Confirm Booking", width=30, height=2, 
                  bg="green", fg="white", command=confirm).pack(pady=15)
        tk.Button(frame, text="Back", width=30, bg="gray", 
                  command=lambda: self.room_GUI([room], prefs)).pack()

    def show_confirmation(self, conf_num, name, email, phone, prefs, room, total):
        """Show confirmation screen"""
        self.clear_screen()
        frame = tk.Frame(self.root, bg="lightgreen")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame
        tk.Label(frame, text="Booking Confirmed!", font=("Times New Roman", 20, "bold"), 
                 bg="lightgreen").pack(pady=20)
        tk.Label(frame, text=f"Confirmation #: {conf_num}", font=("Times New Roman", 14, "bold"), 
                 bg="lightgreen", fg="blue").pack(pady=5)
        tk.Label(frame, text=f"Name: {name}\nEmail: {email}\nPhone: {phone}", 
                 font=("Times New Roman", 11), bg="lightgreen").pack(pady=5)
        tk.Label(frame, text=f"Room: {room.room_type}\nCheck-in: {prefs['check_in']}\n"
                 f"Check-out: {prefs['check_out']}\nTotal: ${total:.2f}",
                 font=("Times New Roman", 11), bg="lightgreen").pack(pady=10)
        tk.Button(frame, text="Return Home", font=("Times New Roman", 13), width=30, 
                  bg="blue", fg="white", command=self.show_homepage).pack(pady=20)

#from app

    #Modify the reservation seciton

    def show_modify(self):
        """Search for booking to modify"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame
        tk.Label(frame, text="Modify Reservation", font=("Times New Roman", 18, "bold")).pack(pady=20)
        tk.Label(frame, text="Confirmation Number:").pack()
        conf_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
        conf_entry.pack(pady=10)

        def search():
            conf = conf_entry.get()
            booking = find_booking(conf)
            if not booking:
                messagebox.showerror("Error", "Booking not found")
                return
            self.modify_booking(conf, booking)

        tk.Button(frame, text="Search", command=search, bg="blue", 
                  fg="white", width=30).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_homepage, 
                  bg="gray", width=30).pack()

    def modify_booking(self, old_conf, old_booking):
        """Modify booking details"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame
        tk.Label(frame, text="Modify Booking", font=("Times New Roman", 16, "bold")).pack(pady=10)

        #Old booking
        old_frame = tk.LabelFrame(frame, text="Current Booking", padx=10, pady=10, bg="lightyellow")
        old_frame.pack(fill="x", pady=10)
        tk.Label(old_frame, text=f"Room: {old_booking['room_type']}\n"
                f"Check-in: {old_booking['check_in']}\n"
                f"Check-out: {old_booking['check_out']}\n"
                f"Total: ${old_booking['total_price']}", bg="lightyellow").pack(anchor="w")
        
        #New dates
        new_frame = tk.LabelFrame(frame, text="New Dates", padx=10, pady=10)
        new_frame.pack(fill="x", pady=10)
        tk.Label(new_frame, text="Check-in:").pack()
        check_in_entry = tk.Entry(new_frame, width=20)
        check_in_entry.pack()
        check_in_entry.insert(0, (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"))
        tk.Label(new_frame, text="Check-out:", pady=10).pack()
        check_out_entry = tk.Entry(new_frame, width=20)
        check_out_entry.pack()
        check_out_entry.insert(0, (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))

        #Guest info
        guest_frame = tk.LabelFrame(frame, text="Guest Info", padx=10, pady=10)
        guest_frame.pack(fill="x", pady=10)
        tk.Label(guest_frame, text="Name:").pack()
        name_entry = tk.Entry(guest_frame, width=30)
        name_entry.pack()
        name_entry.insert(0, old_booking['guest_name'])
        tk.Label(guest_frame, text="Email:", pady=10).pack()
        email_entry = tk.Entry(guest_frame, width=30)
        email_entry.pack()
        email_entry.insert(0, old_booking['guest_email'])
        tk.Label(guest_frame, text="Phone:", pady=10).pack()
        phone_entry = tk.Entry(guest_frame, width=20)
        phone_entry.pack()
        phone_entry.insert(0, old_booking['guest_phone'])
        tk.Label(guest_frame, text="Card:", pady=10).pack()
        card_entry = tk.Entry(guest_frame, width=20)
        card_entry.pack()

        def save_changes():
            check_in = check_in_entry.get()
            check_out = check_out_entry.get()  
            if not validate_date(check_in) or not validate_date(check_out):
                messagebox.showerror("Error", "Invalid dates")
                return       
            if not card_entry.get():
                messagebox.showerror("Error", "Enter card")
                return
            nights = (validate_date(check_out) - validate_date(check_in)).days
            if nights <= 0:
                messagebox.showerror("Error", "Invalid date range")
                return            
            room = next((r for r in self.rooms if r.room_type == old_booking['room_type']), None)
            new_total = nights * room.price
            new_conf = generate_conf_number()
            # Cancel old, create new
            update_booking_status(old_conf, "CANCELLED")
            new_booking = {
                "confirmation_number": new_conf,
                "room_id": room.room_id,
                "guest_name": name_entry.get(),
                "guest_email": email_entry.get(),
                "guest_phone": phone_entry.get(),
                "room_type": room.room_type,
                "check_in": check_in,
                "check_out": check_out,
                "nights": nights,
                "total_price": new_total,
                "status": "CONFIRMED"
            }
            save_booking(new_booking)

            #Send emails
            email_msg = (f"Booking modified!\nNew Confirmation: {new_conf}\n"
                        f"Old Confirmation: {old_conf}\n"
                        f"New Check-in: {check_in}\nNew Check-out: {check_out}\n"
                        f"New Total: ${new_total:.2f}")
            self.send_email(email_entry.get(), "Booking Modified", email_msg)
            messagebox.showinfo("Success", f"Modified! New Conf: {new_conf}")
            self.show_homepage()

        tk.Button(frame, text="Save Changes", width=30, height=2, 
                  bg="green", fg="white", command=save_changes).pack(pady=15)
        tk.Button(frame, text="Back", width=30, bg="gray", 
                  command=self.show_homepage).pack()

    #Cancel Section

    def show_cancel(self):
        """Search for booking to cancel"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        tk.Label(frame, text="Cancel Reservation", font=("Times New Roman", 18, "bold")).pack(pady=20)
        tk.Label(frame, text="Confirmation Number:").pack()
        conf_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
        conf_entry.pack(pady=10)

        def search():
            conf = conf_entry.get()
            booking = find_booking(conf)
            if not booking:
                messagebox.showerror("Error", "Booking not found")
                return
            self.confirm_cancel(conf, booking)

        tk.Button(frame, text="Search", command=search, bg="blue", 
                  fg="white", width=30).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_homepage, 
                  bg="gray", width=30).pack()

    def confirm_cancel(self, conf_num, booking):
        """Confirm cancellation"""
        self.clear_screen()
        frame = tk.Frame(self.root, bg="lightyellow")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        tk.Label(frame, text="Confirm Cancellation", font=("Times New Roman", 16, "bold"), 
                 bg="lightyellow").pack(pady=10)

        info_frame = tk.LabelFrame(frame, text="Booking", padx=10, pady=10, bg="lightyellow")
        info_frame.pack(fill="x", pady=10)

        tk.Label(info_frame, text=f"Confirmation: {conf_num}\nGuest: {booking['guest_name']}\n"
                f"Room: {booking['room_type']}\nCheck-in: {booking['check_in']}\n"
                f"Total: ${booking['total_price']}", bg="lightyellow").pack(anchor="w")

        def cancel():
            update_booking_status(conf_num, "CANCELLED")
            cancel_conf = f"CANCEL-{generate_conf_number()}"
            
            email_msg = (f"Your booking has been cancelled.\n"
                        f"Original Confirmation: {conf_num}\n"
                        f"Cancellation Confirmation: {cancel_conf}\n"
                        f"Thank you!")
            self.send_email(booking['guest_email'], "Booking Cancelled", email_msg)
            
            messagebox.showinfo("Success", f"Cancelled! Conf: {cancel_conf}")
            self.show_homepage()

        tk.Button(frame, text="Confirm Cancellation", command=cancel, bg="red", 
                  fg="white", width=30, height=2).pack(pady=20)
        tk.Button(frame, text="Keep Booking", command=self.show_homepage, 
                  bg="green", fg="white", width=30).pack()

    #Admin Report Section

    def show_login(self):
        """Admin login"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame
        tk.Label(frame, text="Admin Login", font=("Times New Roman", 18, "bold")).pack(pady=20)
        tk.Label(frame, text="Username:").pack(pady=5)
        user_entry = tk.Entry(frame, width=30)
        user_entry.pack()
        tk.Label(frame, text="Password:").pack(pady=5)
        pass_entry = tk.Entry(frame, width=30, show="*")
        pass_entry.pack()
        def login():
            if user_entry.get() == self.admin_user and pass_entry.get() == self.admin_pass:
                self.show_report_options()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        tk.Button(frame, text="Login", command=login, bg="blue", 
                  fg="white", width=30).pack(pady=20)
        tk.Button(frame, text="Back", command=self.show_homepage, 
                  bg="gray", width=30).pack()

    def show_report_options(self):
        """Report options"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        tk.Label(frame, text="Report Options", font=("Times New Roman", 18, "bold")).pack(pady=20)
        report_type = tk.StringVar(value="all")
        tk.Radiobutton(frame, text="All Bookings", variable=report_type, 
                       value="all").pack(anchor="w", padx=20, pady=5)
        tk.Radiobutton(frame, text="Custom Date Range", variable=report_type, 
                       value="custom").pack(anchor="w", padx=20, pady=5)

        date_frame = tk.LabelFrame(frame, text="Dates", padx=10, pady=10)
        date_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(date_frame, text="Start Date:").pack()
        start_entry = tk.Entry(date_frame, width=20)
        start_entry.pack()
        start_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        tk.Label(date_frame, text="End Date:", pady=10).pack()
        end_entry = tk.Entry(date_frame, width=20)
        end_entry.pack()
        end_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def generate():
            bookings = load_bookings()
            
            if report_type.get() == "custom":
                start = validate_date(start_entry.get())
                end = validate_date(end_entry.get())
                if not start or not end:
                    messagebox.showerror("Error", "Invalid dates")
                    return
                bookings = [b for b in bookings 
                           if start <= validate_date(b['check_in']) <= end]

            self.show_report(bookings)

        tk.Button(frame, text="Generate", command=generate, bg="green", 
                  fg="white", width=30).pack(pady=20)
        tk.Button(frame, text="Back", command=self.show_homepage, 
                  bg="gray", width=30).pack()

    def show_report(self, bookings):
        """Display report"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        tk.Label(frame, text="Hotel Booking Report", font=("Times New Roman", 18, "bold")).pack(pady=10)

        # Calculate stats
        total_revenue = sum(b.get('total_price', 0) for b in bookings 
                           if b.get('status') == 'CONFIRMED')
        confirmed = sum(1 for b in bookings if b.get('status') == 'CONFIRMED')
        cancelled = sum(1 for b in bookings if b.get('status') == 'CANCELLED')

        # Create report text
        report = f"""HOTEL BOOKING REPORT
{'='*50}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

SUMMARY:
Total Bookings: {len(bookings)}
Confirmed: {confirmed}
Cancelled: {cancelled}
Total Revenue: ${total_revenue:.2f}
Average Value: ${total_revenue/confirmed if confirmed > 0 else 0:.2f}

{'='*50}
DETAILS:
"""
        for b in bookings:
            report += f"""
Confirmation: {b.get('confirmation_number')}
Guest: {b.get('guest_name')}
Email: {b.get('guest_email')}
Room: {b.get('room_type')}
Check-in: {b.get('check_in')}
Check-out: {b.get('check_out')}
Total: ${b.get('total_price')}
Status: {b.get('status')}
{'-'*50}"""

        text_area = scrolledtext.ScrolledText(frame, width=80, height=20, font=("Courier", 9))
        text_area.pack(pady=10, fill="both", expand=True)
        text_area.insert(tk.END, report)
        text_area.config(state=tk.DISABLED)

        def save():
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            messagebox.showinfo("Success", f"Saved: {filename}")
        tk.Button(frame, text="Save Report", command=save, bg="green", 
                  fg="white", width=30).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_homepage, 
                  bg="gray", width=30).pack()

#RUN APP  (Pray it works! JK it should work)
'''
if __name__ == "__main__":
    root = tk.Tk()
    app = BestHotelBookingGroup(root)
    root.mainloop()
