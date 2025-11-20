"""
Hotel Booking System - User Interface

This module contains the main HotelBookingApp class which handles all user interface 
screens and user interactions

Classes:
    HotelBookingApp: Main application controller
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta

# Import from other modules
from models import Room
from utils import validate_date, generate_conf_number
#from storage import load_bookings, find_booking
from createReservation_logic import create_reservation, modify_reservation, cancel_reservation
from room_logic import get_available_rooms
#from email_service import send_email

class HotelBookingApp:
    """
    Main Hotel Booking Application

    This is the central controller that manages all user interface screens, user interactions,
    and coordinates between business logic and UI

    Attributes:
        root (tk.Tk): Main tkinter window
        rooms (list): List of available room objects
        admin_user (str): Admin username
        admin_pass (str): Admin password
        email_sender (str): Email address for notifications
        email_password (str): Email password fro SMTP
        current_frame (tk.frame): Currently displayed frame

    Example:
        >>> root = tk.Tk()
        >>> app = HotelBookingApp(root)
        >>> root.mainloop()
    """

    def __init__(self, root):
        """
        Initialize the Hotel Booking Application

        Sets up the main window, initializes room data, and displays the homepage

        Args: 
            root (tk.Tk): The main tkinter window
        """
        self.root = root
        self.root.title("Hotel Booking System")
        self.root.geometry("900x800")

        # Initialize room data - 3 room types available
        self.rooms = [
            Room("R001", "Single", 1, 1, 100.0, ["WiFi", "AC"]),
            Room("R002", "Double", 2, 1, 150.0, ["WiFi", "AC", "Bathtub"]),
            Room("R003", "Suite", 4, 2, 250.0, ["WiFi", "AC", "Bathtub", "Mini Bar"])
        ]

        # Admin credentials for report access
        self.admin_user = "admin"
        self.admin_pass = "admin123"

        # Email configuration - UPDATE THESE WITH YOUR EMAIL
        self.email_sender = "your_hotel_email@gmail.com"
        self.email_password = "your_app_password" # user Gmail app password

        # Track current frame for clearing
        self.current_frame = None

        # Show homepage
        self.show_homepage()

    def clear_screen(self):
        """
        Clear the current frame and prepare for new content.
        
        This method destroys the current frame to make room for the next screen.
        This is called at the beginning of every screen method.
        """
        if self.current_frame:
            self.current_frame.destroy()

    def show_homepage(self):
        """
        Display the main homepage with navigation buttons.
        
        Shows four main options:
        - Create New Reservation (Green)
        - Modify Reservation (Orange)
        - Cancel Reservation (Red)
        - Generate Admin Report (Purple)
        
        This is the first screen users see.
        """
        self.clear_screen()
        
        # Create main frame with light blue background
        frame = tk.Frame(self.root, bg="lightblue")
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        # Title
        tk.Label(frame, text="🏨 Hotel Booking System", 
                font=("Arial", 24, "bold"), bg="lightblue").pack(pady=30)
        tk.Label(frame, text="Welcome to Hotel Management", 
                font=("Arial", 12), bg="lightblue").pack(pady=10)

        # Create Reservation Button
        tk.Button(frame, text="✨ Create Reservation", 
                 font=("Arial", 12), bg="green", fg="white",
                 command=self.booking_step1, width=30, height=2).pack(pady=10)
        
        # Modify Reservation Button
        tk.Button(frame, text="📝 Modify Reservation", 
                 font=("Arial", 12), bg="orange", fg="white",
                 command=self.show_modify, width=30, height=2).pack(pady=10)
        
        # Cancel Reservation Button
        tk.Button(frame, text="❌ Cancel Reservation", 
                 font=("Arial", 12), bg="red", fg="white",
                 command=self.show_cancel, width=30, height=2).pack(pady=10)
        
        # Admin Report Button
        tk.Button(frame, text="📊 Admin Report", 
                 font=("Arial", 12), bg="purple", fg="white",
                 command=self.show_login, width=30, height=2).pack(pady=10)
        
    # =========== BOOKING FLOW (3 STEPS) ===========
    def booking_step1(self):
        """
        Display booking step 1: Guest preferences.

        Allows user to enter:
            - Check-in date
            - Check-out date
            - Number of guests
            - Number of beds
            - Preferred amenities
        
        User clicks "Search Rooms" to proceed to step 2
        """
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand= True, padx=20,pady=20)
        self.current_frame=frame

        # Title
        tk.Label(frame, text="Step 1: Your Preferences", font=("Arial",16,"bold")).pack(pady=10)

        # Check-In Date Input
        tk.Label(frame,teext="Check-In (YYYY-MM-DD):").pack()
        check_in_entry = tk.Entry(frame,width=20)
        check_in_entry.pack()
        check_in_entry.insert(0, (datetime.now() + timedelta(day=2)).strftime("%Y-%m-%d"))

        # Check-Out Date Input
        tk.Label(frame, text="Check-Out (YYYY-MM-DD):",pady=10).pack()
        check_out_entry = tk.Entry(frame,width=20)
        check_out_entry.pack()
        check_out_entry.insert(0, (datetime.now() + timedelta(day=2)).strftime("%Y-%m-%d"))

        # Number of guests dropdown menu
        tk.Label(frame, text="Guests:",pady=10).pack()
        guests_var = tk.StringVar(value="1")
        ttk.Combobox(frame, textvariable=guests_var, values=["1","2","3","4"],width=10,state="readonly").pack()

        # Number of beds dropdown menu
        tk.Label(frame, text="Beds:",pady=10).pack()
        beds_var = tk.StringVar(value="1")
        ttk.Combobox(frame, textvariable=guests_var, values=["1","2","3"],width=10,state="readonly").pack()

        # Amenities checkbox selection
        tk.Label(frame, text="Amenities:",pady=10).pack()
        amenity_check={}
        for amenity in ["Wifi","AC", "Bathtub", "Mini Bar"]:
            var = tk.BooleanVar()
            tk.Checkbutton(frame,text=amenity, variable=var).pack(anchor="w",padx=20)
            amenity_check[amenity] = var

        def search():
            "Handle Search Button - validate and proceed to step 2"
            # Get User Input
            check_in = check_in_entry.get()
            check_out = check_out_entry.get()

            # Validate Dates
            if not validate_date(check_in) or not validate_date(check_out):
                messagebox.showerror("ERROR", "Invalid date format. Use YYYY-MM-DD")
                return
            
            # Check that check-out is after check-in
            if validate_date(check_out) <= validate_date(check_in):
                messagebox.showerror("ERROR", "Check-out date must be after check-in date")
                return

            # Get Selected Amenities
            amenities = [a for a, v in amenity_check.items() if v.get()]

            # Get available rooms based on filters
            available = get_available_rooms(
                self.rooms, check_in, check_out,
                int(guests_var.get()), int(beds_var.get()), amenities
                )
            
            # Check if any rooms available
            if not available:
                messagebox.showerror(
                    "No Availability",
                    "No rooms match your criteria.\nTry different dates or preferences."
                    )
                return
            
            # Store preferences and proceed to step 2
            prefs={
                "check_in":check_in,
                "check_out":check_out,
                "nights": (validate_date(check_out) - validate_date(check_in)).days
            }
            self.booking_step2(available, prefs)

        # Buttons
        tk.Button(frame, text="Search Rooms", command=search, width=30,
                  height=2, bg="blue", fg="white", font=("Arial", 12)).pack(pady=15)
        tk.Button(frame, text="Back", command=self.show_homepage, width=30,
                  bg="gray", font=("Arial", 11)).pack()
        
    def booking_step2(self, available_rooms, prefs):
        """
        Display Booking Step 2: Room Selection

        Show list of available rooms with details:
            - Room Type
            - Number of Beds
            - Amenities
            - Nightly Rate
            - Total Price for Duration
        
        User selects room and clicks "Continue" to proceed to step 3

        Args:
            available_rooms (list): List of Available Room Objects
            prefs (dict): Preferences from step 1
        """   
        self.clear_screen()
        frame = tk.Frame(self.root).pack(fill="both", expand=True,padx=20,pady=20)
        self.current_frame = frame

        # Title
        tk.Label(frame, text="Step 2: Select Room", font=("Arial", 16, "bold")).pack(pady=10)

        # Show Dates Summary
        summary_text = f"{prefs['check_in']} to {prefs['check_out']} ({prefs['nights']} nights)"
        tk.Label(frame, text=summary_text, bg="lightyellow",padx=10,pady=5).pack(fill="x",pady=10)

        # Room Selection Variable
        room_var = tk.StringVar()

        # Create Scrollable Frame for Rooms
        room_frame = tk.Frame(frame, bg="lightgray", relief="sunken", bd=1)
        room_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(room_frame, bg="lightgray")
        scrollbar = ttk.Scrollbar(room_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="lightgray")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right",fill="y")

        # Display Each Available Room
        for room in available_rooms:
            # Calculate Total Price
            total = prefs['nights'] * room.price
            amenity_str = ",".join(room.amenities)

            # Create Room Display Box
            room_box = tk.Frame(scroll_frame, bg="white", relief="ridge", bd=2)
            room_box.pack(fill="x", padx=5, pady=5)

            # Room Selection Radio Button
            tk.Radiobutton(room_box, text=f"{room.room_type} - ${room.price}/night", variable=room_var,
                           value=room.room_id, font=("Arial", 11), bg="white").pack(anchor="w", padx=10, pady=5)
            
            # Room Details
            details_text = (f"Beds: {room.num_beds} | "
                            f"Amenities: {amenity_str}\n"
                            f"Total for {prefs['nights']} night(s): ${total:.2f}")
            tk.Label(room_box, text=details_text, font=("Arial",9), bg="white",
                     fg="darkblue").pack(anchor="w", padx=30)
        
        def next_step():
            """Proceed to step 3 if room selected"""
            if not room_var.get():
                messagebox.showerror("ERROR", "Please select a room")
                return
            
            # Get Selected Room
            selected_room = next((r for r in available_rooms if r.room_id == room_var.get()), None)

            # Create Booking Info and proceed to step 3
            booking_info = {
                "prefs" : prefs,
                "room": selected_room,
                "total": prefs['nights'] * selected_room.price
            }
            self.booking_step3(booking_info)

        # Buttons
        tk.Button(frame, text="Continue", command=next_step, width=30,
                  height=2, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(frame, text="Back", command=lambda: self.booking_step1(), width=30,
                  bg="gray", font=("Arial", 11)).pack()

    def booking_step3(self, booking_info):
        """
        Display Booking Step 3: Guest Details and Confirmation

        Ask User to Enter:
            - Full Name
            - Email Address
            - Phone Number
            - Credit Card Number

        Shows booking summary and allows user to confirm

        Args:
            booking_info (dict): Room and preferences from steps 1 and 2
        """
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        # Title
        tk.Label(frame, text="Step 3: Guest Details", font=("Arial", 16, "bold")).pack(pady=10)

        # Booking SUmmary
        summary_frame = tk.LabelFrame(frame, text="Booking Summary", padx=10,pady=10, bg="lightblue")
        summary_frame.pack(fill="x", pady=10)

        room = booking_info["room"]
        prefs = booking_info["prefs"]
        summary_text = (f"Room: {room.room_type} | "
                        f"Check-in: {prefs['check_in']}\n"
                        f"Check-out: {prefs['check_out']} | "
                        f"Total: ${booking_info['total']:.2f}")
        tk.Label(summary_frame, text=summary_text, bg="lightblue").pack(anchor="w")

        # Guest Information Form
        tk.Label(frame, text="Name:", pady=10).pack()
        name_entry = tk.Entry(frame,width=30)
        name_entry.pack()

        tk.Label(frame, text="Email:", pady=10).pack()
        email_entry = tk.Entry(frame,width=30)
        email_entry.pack()

        tk.Label(frame, text="Phone:", pady=10).pack()
        phone_entry = tk.Entry(frame,width=20)
        phone_entry.pack()

        tk.Label(frame, text="Card Number:", pady=10).pack()
        card_entry = tk.Entry(frame,width=20)
        card_entry.pack()

        def confirm():
            """Confirm Booking and Send Email"""
            # Validate All Fields Filled
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            card = card_entry.get()

            if not all([name, email, phone, card]):
                messagebox.showerror("ERROR", "Please fill all fields")
                return
            
            # Create Booking Using Business Logic
            guest_info = {
                'name': name,
                'email': email,
                'phone': phone,
                'card': card
            }

            booking= create_reservation(guest_info, room, prefs, self.email_sender, self.email_password)

            # Show Confirmation Screen
            self.show_confirmation(booking, room, prefs)

        # Buttons
        tk.Button(frame, text="Confirm Booking", command=confirm, width=30,
                  height=2, bg="green", fg="white", font=("Arial", 12)).pack(pady=15)
        tk.Button(frame, text="Back", command=lambda: self.booking_step2([room], prefs), width=30,
                  bg="gray", font=("Arial", 11)).pack()
        
    def show_confirmation(self, booking, room, prefs):
        """
        Display Booking Confirmation Screen

        Shows:
            - Confirmation Number
            - Guest Details
            - Room and Dates
            - Total Price
            - Message that email has been sent

        Args:
            booking (dict): booking data
            room (Room): Booked room object
            prefs (dict): Booking preferences
        """
        self.clear_screen()
        frame = tk.Frame(self.root, bg="lightgreen")
        frame.pack(fill="both", expand=True, padx=20,pady=20)
        self.current_frame = frame

        #Title
        tk.Label(frame, text = "✅ Booking Confirmed!", font=("Arial",14,"bold"),
                 bg="lightgreen", fg="blue").pack(pady=5)
        
        # Confirmation Number
        tk.Label(frame, text=f"Confirmation #: {booking['confirmation_number']}",
                 font=("Arial",14,"bold"), bg="lightgreen", fg="blue").pack(pady=5)
        
        # Guest Info
        tk.Label(frame, text=f"Name: {booking['guest_name']}\n"
                 f"Email: {booking['guest_email']}\n"
                 f"Phone: {booking['guest_phone']}",
                 font=("Arial",11), bg="lightgreen").pack(pady=5)
        
        # Room and Dates
        tk.Label(frame,text=f"Room: {room.room_type}\n"
                 f"Check-in: {prefs['check_in']}\n"
                 f"Check-out: {prefs['check_out']}\n"
                 f"Total: ${booking['total_price']:.2f}",
                 font=("Arial",11), bg="lightgreen").pack(pady=10) 
        
        # Email Notification
        tk.Label(frame, text="📧 Confirmation email has been sent", bg="lightgreen",
                 font=("Arial",10, "italic"), fg="darkgreen").pack(pady=10)
        
        # Return Button
        tk.Button(frame, text="Return to Homepage", font=("Arial",13), width=30, bg="blue",
                  fg="white", command=self.show_homepage).pack(pady=20)
        
    # =========== MODIFY RESERVATION ===========
    def show_modify(self):
        """
        Display modify reservation screen

        Ask user for confirmation number of existing booking.
        Searches for booking and proceeds to modification screen if found
        """
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20,pady=20)
        self.current_frame = frame

        tk.Label(frame, text="Modify Reservation", font=("Arial",18, "bold")).pack(pady=20)
        tk.Label(frame, text="Confirmation Number:").pack()

        conf_entry = tk.Entry(frame, width=30, font=("Arial",12))
        conf_entry.pack(pady=10)

        def search():
            """Search for Booking"""
            conf = conf_entry.get()
            booking = find_booking(conf)
            if not booking:
                messagebox.showerror("ERROR", "Booking Not Found")
                return
            self.modify_booking_screen(conf, booking)

        tk.Button(frame, text="Search", command=search, bg="blue", fg="white", width=30).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_homepage, bg="gray", width=30).pack()

    def modify_booking_screen(self, old_conf, old_booking):
        """Modify Booking Screen - allow user to change dates and details"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        tk.Label(frame, text="Modify Reservation", font=("Arial", 16, "bold")).pack(pady=10)

        # Current Booking
        old_frame = tk.LabelFrame(frame, text="Current Booking",padx=10,pady=10,bg="lightyellow")
        old_frame.pack(fill="x", pady=10)
        tk.Label(old_frame, text=f"room: {old_booking['room_type']}\n"
                 f"Check-in: {old_booking['check_in']}\n"
                 f"Check-out: {old_booking['check_out']}\n"
                 f"Total: ${old_booking['total_price']}",
                 bg="lightyellow").pack(anchor="w")
        
        # New Dates
        new_frame = tk.LabelFrame(frame, text="New Dates", padx=10,pady=10)
        new_frame.pack(fill="x",pady=10)

        tk.Label(new_frame, text="Check-in:").pack()
        check_in_entry = tk.Entry(new_frame, width=20)
        check_in_entry.pack()
        check_in_entry.insert(0, (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))

        tk.Label(new_frame, text="Check-in:").pack()
        check_out_entry = tk.Entry(new_frame, width=20)
        check_out_entry.pack()
        check_out_entry.insert(0, (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))

        # Guest Info
        guest_frame = tk.LabelFrame(frame, text="Guest Info", padx=10, pady=10)
        guest_frame.pack(fill="x",pady=10)

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
            """Save Modifications"""
            check_in = check_in_entry.get()
            check_out = check_out_entry.get()

            if not validate_date(check_in) or not validate_date(check_out):
                messagebox.showerror("ERROR", "Invalid Dates")
                return
            if not card_entry.get():
                messagebox.showerror("ERROR", "Enter Card Number")
                return
            
            nights = (validate_date(check_out) - validate_date(check_in)).days
            if nights <= 0:
                messagebox.showerror("ERROR", "Invalid Date Range")
                return
            
            room = next((r for r in self.rooms if r.room_type == old_booking['room_type']),None)
            new_guest_info = {
                'name': name_entry.get(),
                'email': email_entry.get(),
                'phone': phone_entry.get(),
                'card': card_entry.get()
            }
            new_prefs={
                'check_in': check_in,
                'check-out': check_out,
                'nights': nights
            }

            modify_reservation(old_conf, new_guest_info, new_prefs, room, self.email_sender, self.email_password)
            messagebox.showinfo("SUCCESS", "Reservation modified!")
            self.show_homepage()

        tk.Button(frame, text="Save Changes", command=save_changes, width=30,
                  height=2,bg="green",fg="white").pack(pady=15)
        tk.Button(frame, text="Back", command=self.show_homepage, width=30,
                  bg="gray").pack()
        
    # =========== CANCEL RESERVATION ===========
    def show_cancel(self):
        """Display Cancel Reservation Screen"""
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20,pady=20)
        self.current_frame=frame

        tk.Label(frame, text="Cancel Reservation", font=("Arial",18,"bold")).pack(pady=20)
        tk.Label(frame, text="Confirmation Number:").pack()

        conf_entry = tk.Entry(frame, width=30, font=("Arial",12))
        conf_entry.pack(pady=10)

        def search():
            """Search for Booking"""
            conf = conf_entry.get()
            booking = find_booking(conf)
            if not booking:
                messagebox.showerror("ERROR", "Booking Not Found")
                return
            self.confirm_cancel(conf, booking)
        
        tk.Button(frame, text="Search", command=search, bg="blue",fg="white",width=30).pack(pady=10)
        tk.Button(frame,text="Back", command=self.show_homepage, bg="gray", width=30).pack()

    def confirm_cancel(self,conf_num, booking):
        """Confirm Cancellation"""
        self.clear_screen()
        frame = tk.Frame(self.root, bg="lightyellow")
        frame.pack(fill="both", expand=True, padx=20,pady=20)
        self.current_frame=frame

        tk.Label(frame, text="Confirm Cancellation",font=("Arial",16,"bold"),
                 bg="lightyellow").pack(pady=10)
        
        info_frame = tk.LabelFrame(frame,text="Booking",padx=10,pady=10,bg="lightyellow")
        info_frame.pack(fill="x", pady=10)

        tk.Label(info_frame, text=f"Confirmation: {conf_num}\n"
                 f"Guest: {booking['guest_name']}\n"
                 f"Room: {booking['room_type']}\n"
                 f"Check-in: {booking['check_in']}\n"
                 f"Total: ${booking['total_price']}", bg="lightyellow").pack(anchor="w")

        def cancel():
            """Cancel Booking"""
            cancel_reservation(conf_num, booking, self.email_sender, self.email_password)
            messagebox.showinfo("SUCCESS", "Reservation Cancelled!")
            self.show_homepage()

        tk.Button(frame, text="Confirm Cancellation", command=cancel, bg="red",
                  fg="white", width=30, height=2).pack(pady=20)
        tk.Button(frame, text="Keep Reservation", command=self.show_homepage,
                  bg="green", fg="white", width=30).pack()
        
    # =========== ADMIN REPORT ===========

    print("testing testing")