"""
Hotel Booking Software - UI Display and Management

This module consists of the main HotelBookingApp class which contains additional methods to
help handle the change of screens the user interacts with

Class:
    HotelBookingApp: Main software/project controller
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
from PIL import Image, ImageTk, ImageDraw

# Import from other modules
from models import Room
from utils import validate_date, generate_conf_number, load_bookings, find_booking, save_booking
# from storage import load_bookings, find_booking
from utils import load_bookings, find_booking
from createReservation_logic import create_reservation, modify_reservation, cancel_reservation
from room_logic import get_available_rooms
from email_service import send_email

class BestHotelBookingGroup:
    """
    Main Hotel Booking Software/Project

    This is the main controller that handles GUI, user interactions, and verifies selections,ID's, and reservations
    with the help of other classes such as business logic

    This is the class that main.py calls to run the program

    Attributes:
        root (tk.Tk): Main tkinter window
        rooms (list): List of available room objects
        admin_user (str): Admin username
        admin_pass (str): Admin password
        email_sender (str): Email address for notifications
        email_password (str): Email password fro SMTP
        current_frame (tk.frame): Currently displayed frame

    How Main.py calls this class to run program:
        >>> root = tk.Tk()
        >>> app = HotelBookingApp(root)
        >>> root.mainloop()
    """
    #Matthew Cabrera 11/21/2025 I worked on a lot of the tkinter methods in app
    def __init__(self, root):
        """
        Initialize the Program

        Sets up the main window (start screen) which first displays the homescreen and initializes room info

        Args: 
            root (tk.Tk): The main tkinter window
        """
        self.root = root
        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.rooms = [
            Room("R000", "Single", 1, 1, 100.0, ["None"]),
            Room("R001", "Double", 1, 1, 150.0, ["None"]),
            Room("R002", "Suite", 1, 1, 300.0, ["None"]),
            Room("R003", "Single", 1, 1, 110.0, ["\U0001F4F6 WiFi - $10 "]),
            Room("R004", "Double", 1, 1, 125.0, ["\U0001F321 Air Conditoning - $25"]),
            Room("R005", "Suite", 4, 2, 538.0, ["\U0001F6C1 Bathtub - $38"]),
            Room("R006", "Suite", 4, 2, 552.0, ["\U0001F37A Mini-Fridge - $52"]),
            Room("R007", "Single", 1, 1, 135.0, ["\U0001F4F6 WiFi - $10 ", "\U0001F321 Air Conditoning - $25"]),
            Room("R008", "Double", 2, 1, 223.0, ["\U0001F4F6 WiFi - $10 ", "\U0001F321 Air Conditoning - $25", "\U0001F6C1 Bathtub - $38"]),
            Room("R009", "Suite", 4, 2, 340.0, ["\U0001F6C1 Bathtub - $38", "\U0001F37A Mini-Fridge - $52"]),
            Room("R0010", "Suite", 4, 2, 323.0, ["\U0001F4F6 WiFi - $10 ", "\U0001F321 Air Conditoning - $25", "\U0001F6C1 Bathtub - $38"]),
            Room("R0011", "Suite", 4, 2, 375.0, ["\U0001F4F6 WiFi - $10 ", "\U0001F321 Air Conditoning - $25", "\U0001F6C1 Bathtub - $38", "\U0001F37A Mini-Fridge - $52"])
        ]

        #Admin credentials for report access
        self.admin_user = "admin"
        self.admin_pass = "admin123"

        #Email configuration
        self.email_sender = os.environ.get("user_email", "")
        self.email_password = os.environ.get("user_pass", "") #Use User Gmail App Password

        #Track current frame for clearing
        self.current_frame = None

        #Show homepage
        self.show_homepage()

    def createButton(self,buttonText,color,toDo,space,size):
        """This creates similar buttons so code doesn't duplicate"""
        tk.Button(self.current_frame, text=buttonText, 
                font=("Times New Roman", size), bg=color, fg="lemon chiffon",
                command=toDo, width=30, height=2).pack(pady=space)

    def clear_screen(self):
        """
        This clears the current frame
        Allows for new menu displays to takeover frame
        """
        if self.current_frame:
            self.current_frame.destroy()

    def updateScreen(self,bColor,xSize,ySize):
        """
        Updates the window screen to display the new function/menu
        Clears the window to show new interactive menu
        """
        self.clear_screen()
        if bColor is None:
            frame = tk.Frame(self.root)
        else: 
            frame = tk.Frame(self.root,bg=bColor)
        frame.pack(fill="both", expand= True, padx=xSize,pady=ySize)
        #self.clear_screen()
        self.current_frame=frame

    def search(self,conf_entry,method):
            """
            Checks if Reservation Exists
            Passes user to corresponding method
            Example:
                if cancelling
                    ----> confirm_cancel
                if modifying
                    ----> modify_booking_screen
            """
            conf = conf_entry.get()
            booking = find_booking(conf)
            if not booking:
                messagebox.showerror("ERROR", "Reservation Not Found")
                return
            method(conf, booking)

    def show_homepage(self):
        #Matthew Cabrera 11/21/2025
        """
        #Current backdrop may be changed in the future
        Display the homepage with buttons for all 4 functions.
        
        Contains buttons for the following functions:
            - Create New Reservation (Green)
            - Modify Reservation (Orange)
            - Cancel Reservation (Red)
            - Generate Admin Report (Purple)
        
        The first screen users will see when launching program.
        """
        #Update screen with new menu display
        self.updateScreen(bColor="lemon chiffon",xSize=0,ySize=0)
        #Title
        #degree_symbol = "\u00B0"
        
        tk.Label(self.current_frame, text=" \U0001F3E8 Hotel Enigma", 
                font=("Georgia", 30, "bold"), bg="lemon chiffon").pack(pady=30)
        tk.Label(self.current_frame, text="Take your first step with us", 
                font=("Montserrat", 20, "bold", "italic"), bg="lemon chiffon").pack(pady=10)
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "imageResources", "hotel1.jpg")
        image = Image.open(image_path)
        image = image.resize((450, 300), Image.LANCZOS)  # Resize image to fit
        rounded_image = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image)
        image_label = tk.Label(self.current_frame, image=photo, bg="lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 60, y = 420)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path2 = os.path.join(BASE_DIR, "imageResources", "hotelpool.jpg")
        image = Image.open(image_path2)
        image = image.resize((500, 500), Image.LANCZOS)  # Resize image to fit
        rounded_image2 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image2)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 970, y = 220)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path3 = os.path.join(BASE_DIR, "imageResources", "hotelguest.jpg")
        image = Image.open(image_path3)
        image = image.resize((450, 350), Image.LANCZOS)  # Resize image to fit
        rounded_image3 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image3)
        image_label = tk.Label(self.current_frame, image=photo, bg="lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 60, y = 50)

        #image_label.pack(pady=0)  # Add some padding around the image
        #Create Reservation Button
        self.createButton(buttonText="Book your stay with us here!", color="#023553", toDo=self.preferences, space=10, size = 12)
        #Modify Reservation Button
        self.createButton(buttonText="Need to make a change? Click here!", color="#023553", toDo=self.show_modify, space= 10, size = 12)
        #Cancel Reservation Button
        self.createButton(buttonText="Something's come up? Cancel here!", color="#023553", toDo=self.show_cancel, space = 10, size = 12)
        #Admin Report Button
        self.createButton(buttonText="Admin Report", color="#023553", toDo=self.show_login, space=10,size=12)


        #RELOCATE BUTTON 
        #button1 = tk.Button(self.current_frame, text="Book your stay with us here!", command=self.preferences, bg="#023553", fg="lemon chiffon")
        #button1.place(x=100, y=150) 
        
    def create_rounded_image(self, image, radius):
        """
        Create a rounded image with the specified radius.

        Args:
            image (PIL.Image): The original image to be rounded.
            radius (int): The radius for the rounded corners.

        Returns:
            PIL.Image: The rounded image.
        """
        # Create a mask for the rounded corners
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
        
        # Apply the mask to the image
        rounded_image = Image.new('RGBA', image.size)
        rounded_image.paste(image, (0, 0), mask)
        return rounded_image
        
    #Resrvation
    def preferences(self):
        """
        Displays first step for creating a reservation.

        Allows user to enter/interact with:
            - Check-in date
            - Check-out date
            - Number of guests
            - Number of beds
            - Preferred amenities
        
        User clicks "Search Rooms" to validate selections and to continue
        the reservation process
        """
        #Update screen with new menu display
        self.updateScreen(bColor="lemon chiffon",xSize=0,ySize=0)
        #Title
        tk.Label(self.current_frame, text="Choose your preferences!", font=("Times New Roman", 16, "bold"), bg=("lemon chiffon")).pack(pady=10)
        #Check-In Date Input
        tk.Label(self.current_frame,text="Tell us your Check-In dates! (YYYY-MM-DD):", font=("Times New Roman", 12, "bold"), bg=("lemon chiffon")).pack()
        check_in_entry = tk.Entry(self.current_frame,width=20)
        check_in_entry.pack()
        check_in_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        #Check-Out Date Input
        tk.Label(self.current_frame, text="Tell us your Check-Out dates! (YYYY-MM-DD):", font=("Times New Roman", 12, "bold"), bg=("lemon chiffon"),pady=10).pack()
        check_out_entry = tk.Entry(self.current_frame,width=20)
        check_out_entry.pack()
        check_out_entry.insert(0, (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"))

        #Images in screen
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "imageResources", "room2.jpg")
        image = Image.open(image_path)
        image = image.resize((500, 400), Image.LANCZOS)  # Resize image to fit
        rounded_image = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image)
        image_label = tk.Label(self.current_frame, image=photo, bg="lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 960, y = 350)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path2 = os.path.join(BASE_DIR, "imageResources", "room1.jpg")
        image = Image.open(image_path2)
        image = image.resize((500, 400), Image.LANCZOS)  # Resize image to fit
        rounded_image2 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image2)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 50, y = 55)
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path3 = os.path.join(BASE_DIR, "imageResources", "Hotel-fridge.jpg")
        image = Image.open(image_path3)
        image = image.resize((500, 250), Image.LANCZOS)  # Resize image to fit
        rounded_image3 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image3)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 50, y = 500)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path4 = os.path.join(BASE_DIR, "imageResources", "bathtub.jpg")
        image = Image.open(image_path4)
        image = image.resize((500, 250), Image.LANCZOS)  # Resize image to fit
        rounded_image4 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image4)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 960, y = 55)

        #Number of guests dropdown menu
        tk.Label(self.current_frame, text="Guests:", font = ("Times New Roman", 12, "bold"), bg=("lemon chiffon"),pady=10).pack()
        guests_var = tk.StringVar(value="1")
        ttk.Combobox(self.current_frame, textvariable=guests_var, values=["1", "2", "3", "4"], width=10, state="readonly").pack()
        #Number of beds dropdown menu
        tk.Label(self.current_frame, text="Beds:", font = ("Times New Roman", 12, "bold"), bg=("lemon chiffon"), pady=10).pack()
        beds_var = tk.StringVar(value="1")
        ttk.Combobox(self.current_frame, textvariable=beds_var, values=["1", "2", "3"], width=10, state="readonly").pack()
        #Amenities checkbox selection, we need to add more later guys
        tk.Label(self.current_frame, text="Amenities:", font = ("Times New Roman", 12, "bold"), bg=("lemon chiffon"), pady=10).pack()
        amenity_check={}
        for amenity in ["\U0001F4F6 WiFi - $10 ", "\U0001F321 Air Conditoning - $25", "\U0001F6C1 Bathtub - $38", "\U0001F37A Mini-Fridge - $52"]:
            var = tk.BooleanVar()
            tk.Checkbutton(self.current_frame,text=amenity, bg=("lemon chiffon"), variable=var).pack(anchor="center",padx=20)
            amenity_check[amenity] = var

        def search():
            "Search Button - validate user selections then if valid go on to step 2"
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
            available = get_available_rooms(self.rooms, check_in, check_out, int(guests_var.get()), int(beds_var.get()), amenities)
            
            # Check if any rooms available
            if not available:
                messagebox.showerror(
                    "None Available",
                    "No rooms match your criteria.\nTry different dates or preferences."
                    )
                return
            
            # Store preferences and proceed to step 2
            prefs={
                "check_in":check_in,
                "check_out":check_out,
                "nights": (validate_date(check_out) - validate_date(check_in)).days
            }
            self.room_GUI(available, prefs)

        # Buttons
        self.createButton(buttonText="Search Rooms",color="#023553",toDo=search,space=15,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=self.show_homepage,space=0,size=11)
        
    def room_GUI(self, available_rooms, prefs):
        """
        Displays second step for creating a room selection: Room Selection

        Show all rooms available that match users criteria/selections:
            - Room Type
            - Number of Beds
            - Amenities
            - Nightly Rate
            - Total Price for Duration
        
        User then selects desired room and clicks "Continue" to go to final step of creating reservation

        Args:
            available_rooms (list): List of Available Room Objects
            prefs (dict): Preferences from step 1
        """   
        #Update screen with new menu display
        self.updateScreen(bColor="lemon chiffon",xSize=0,ySize=0)

        #Title
        tk.Label(self.current_frame, text="Select your desired room!", bg=("lemon chiffon"), font=("Georgia", 22, "bold")).pack(pady=10)

        #Show Dates Selected
        summary_text = f"{prefs['check_in']} to {prefs['check_out']} ({prefs['nights']} nights)"
        tk.Label(self.current_frame, text=summary_text, font = ("Times New Roman", 14, "bold"), bg="lemon chiffon", padx=10, pady=5).pack(fill="x",pady=10)

        #Room Selection Variable
        room_var = tk.StringVar()

        #Create Scrollable Window to view rooms available
        room_frame = tk.Frame(self.current_frame, bg = "lightgray", relief = "sunken", bd = 1)
        room_frame.pack(fill="both", expand=True, padx=10, pady=10)
        canvas = tk.Canvas(room_frame, bg = "lightgray")
        scrollbar = ttk.Scrollbar(room_frame, orient = "vertical", command = canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="lightgray")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right",fill="y")

        # Display All Available Rooms
        for room in available_rooms:
            #Calculate Total Price
            total = prefs['nights'] * room.price
            amenity_str = ",".join(room.amenities)
            #Create Room Display Box
            room_box = tk.Frame(scroll_frame, bg="white", relief="ridge", bd=2)
            room_box.pack(fill="x", padx=5, pady=5)
            #Room Selection Radio Button
            tk.Radiobutton(room_box, text=f"{room.room_type} - ${room.price}/night", variable=room_var,
                           value=room.room_id, font=("Georgia", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)
            #Room Details
            details_text = (f"Beds: {room.num_beds} | "
                            f"Amenities: {amenity_str}\n"
                            f"Total for {prefs['nights']} night(s): ${total:.2f}")
            tk.Label(room_box, text=details_text, font=("Times New Roman", 12, "bold"), bg="white",
                     fg="#023553").pack(anchor="w", padx=30)
        
        def next_step():
            #Matthew Cabrera
            """Move onto step 3 if room was found and user selected a room"""
            if not room_var.get():
                messagebox.showerror("ERROR", "Please select a room")
                return
            
            #Get Selected Room
            selected_room = next((r for r in available_rooms if r.room_id == room_var.get()), None)

            #Create Booking Info and proceed to step 3
            booking_info = {
                "prefs" : prefs,
                "room": selected_room,
                "total": prefs['nights'] * selected_room.price
            }
            self.guest_Details(booking_info)

        #Buttons
        self.createButton(buttonText="Continue",color="#023553",toDo=next_step,space=10,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=lambda: self.preferences(),space=0,size=11)

    def guest_Details(self, booking_info):
        #Matthew Cabrera 11/21/2025
        """
        Display Final Step (step 3): Guest(User) Info and Confirmation

        Ask User to Enter Personal Info:
            - Full Name
            - Email Address
            - Phone Number
            - Credit Card Number

        Last displays reservation summary and lets user confirm reservation

        Args:
            booking_info (dict): Room and user selections from previous steps (steps 1 and 2)
        """
        #Update window with new menu display
        self.updateScreen(bColor="lemon chiffon", xSize = 0, ySize = 0)

        #Title
        tk.Label(self.current_frame, text="Guest Details", font=("Georgia", 22, "bold"), bg=("lemon chiffon")).pack(pady=10)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "imageResources", "contactus.webp")
        image = Image.open(image_path)
        image = image.resize((500, 300), Image.LANCZOS)  # Resize image to fit
        rounded_image = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 970, y = 350)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path2 = os.path.join(BASE_DIR, "imageResources", "guest.jpg")
        image = Image.open(image_path2)
        image = image.resize((540, 590), Image.LANCZOS)  # Resize image to fit
        rounded_image2 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image2)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 45, y = 180)


        #Booking Summary

        
        summary_frame = tk.LabelFrame(self.current_frame, padx = 10, pady= 10, bg="#023553")
        summary_frame.pack(fill="x", pady=10)

        summary_label = tk.Label(summary_frame, text="Reservation Summary", font=("Times New Roman", 16, "bold"), bg="#023553", fg="lemon chiffon")
        summary_label.pack(side="top", anchor="center")

        room = booking_info["room"]
        prefs = booking_info["prefs"]
        summary_text = (f"Room: {room.room_type} | "
                        f"Check-in: {prefs['check_in']}\n"
                        f"Check-out: {prefs['check_out']} | "
                        f"Total: ${booking_info['total']:.2f}")
        tk.Label(summary_frame, text=summary_text, font = ("Times New Roman", 12, "bold"), fg = "lemon chiffon", bg="#023553").pack(anchor="center")

        #Guest Information Form
        tk.Label(self.current_frame, text="Name:", font = ("Times New Roman", 12, "bold"), bg=("lemon chiffon"), pady=10).pack()
        name_entry = tk.Entry(self.current_frame,width=30)
        name_entry.pack()

        tk.Label(self.current_frame, text="Email:", font = ("Times New Roman", 12, "bold"), bg=("lemon chiffon"), pady=10).pack()
        email_entry = tk.Entry(self.current_frame,width=30)
        email_entry.pack()

        tk.Label(self.current_frame, text="Phone:", font = ("Times New Roman", 12, "bold"), bg=("lemon chiffon"), pady=10).pack()
        phone_entry = tk.Entry(self.current_frame,width=20)
        phone_entry.pack()

        tk.Label(self.current_frame, text="Card Number:", font = ("Times New Roman", 12, "bold"), bg=("lemon chiffon"), pady=10).pack()
        card_entry = tk.Entry(self.current_frame,width=20)
        card_entry.pack()

        def confirm():
            """Confirm Reservation and Send User Confirmation Email"""
            #Validate All Fields Filled
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            card = card_entry.get()

            if not all([name, email, phone, card]):
                messagebox.showerror("ERROR", "Please fill all fields")
                return
            
            #Create Booking Using Business Logic
            guest_info = {
                'name': name,
                'email': email,
                'phone': phone,
                'card': card
            }

            booking = create_reservation(guest_info, room, prefs, self.email_sender, self.email_password)

            #Show Confirmation Screen
            self.show_confirmation(booking, room, prefs)

        #Buttons
        self.createButton(buttonText="Confirm Reservation",color="#023553",toDo=confirm,space=15,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=lambda: self.room_GUI([room], prefs),space=0,size=11)
        
    def show_confirmation(self, booking, room, prefs):
        """
        Display Reservation Confirmation Screen

        Displays:
            - Confirmation Number
            - Guest(User) Details
            - Room and Dates Selected
            - Total Price
            - "Message Has Been Sent" Notification/Pop-Up

        Args:
            booking (dict): booking data
            room (Room): Booked room object
            prefs (dict): Booking preferences
        """
        #Update Screen with new menu display
        self.updateScreen(bColor = "lightgreen", xSize = 0, ySize = 0)

        #Title
        tk.Label(self.current_frame, text = "Reservation Confirmed! We hope you enjoy your stay with us at Hotel Enigma", font=("Georgia", 14, "bold"),
                 bg="lightgreen", fg="blue").pack(pady=5)
        
        #Confirmation Number
        tk.Label(self.current_frame, text=f"Your Confirmation # is: {booking['confirmation_number']}",
                 font=("Times New Roman",14,"bold"), bg="lightgreen", fg="blue").pack(pady=5)
        
        #Guest Info
        tk.Label(self.current_frame, text=f"Name: {booking['guest_name']}\n"
                 f"Email: {booking['guest_email']}\n"
                 f"Phone: {booking['guest_phone']}",
                 font=("Times New Roman", 14, "bold"), bg="lightgreen").pack(pady=5)
        
        #Room and Dates
        tk.Label(self.current_frame,text=f"Room: {room.room_type}\n"
                 f"Check-In Date: {prefs['check_in']}\n"
                 f"Check-Out Date: {prefs['check_out']}\n"
                 f"Total: ${booking['total_price']:.2f}",
                 font=("Times New Roman", 14, "bold"), bg="lightgreen").pack(pady=10) 
        
        #Email Notification
        tk.Label(self.current_frame, text="Confirmation Email Has Been Sent", bg="lightgreen",
                 font=("Times New Roman", 18, "italic"), fg="darkgreen").pack(pady=10)
        
        #Return Button
        self.createButton(buttonText="Return to Homepage",color="blue",toDo=self.show_homepage,space=20,size=13)
        
    #Modify Reservation
    def show_modify(self):
        """
        Display Modify Reservation Screen

        Ask user for their confirmation number from an existing reservation
        Sees if reservation exists, if so move onto modify screen
        """
        #Update screen with new menu display
        self.updateScreen(bColor="lemon chiffon", xSize = 0, ySize = 0)

        tk.Label(self.current_frame, text="Modify Reservation", bg=("lemon chiffon"), font=("Georgia", 18, "bold")).pack(pady=20)
        tk.Label(self.current_frame, text="Confirmation Number:", bg=("lemon chiffon"), font=("Helvetica", 12, "bold")).pack()

        conf_entry = tk.Entry(self.current_frame, width=30, font=("Times New Roman",12))
        conf_entry.pack(pady=10)
        method=self.modify_booking_screen

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "imageResources", "desk.jpg")
        image = Image.open(image_path)
        image = image.resize((600, 400), Image.LANCZOS)  #Resize image to fit
        rounded_image = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image)
        image_label = tk.Label(self.current_frame, image=photo, bg="lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x=50, y=350)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path2 = os.path.join(BASE_DIR, "imageResources", "reservation.jpg")
        image = Image.open(image_path2)
        image = image.resize((600, 400), Image.LANCZOS)  #Resize image to fit
        rounded_image2 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image2)
        image_label = tk.Label(self.current_frame, image=photo, bg="lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x=875, y=370)             

        #Buttons
        self.createButton(buttonText="Search",color="#023553",toDo=lambda: self.search(conf_entry, method),space=10,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=self.show_homepage,space=0,size=12)

    def modify_booking_screen(self, old_conf, old_booking):
        """
        Modify Reservation Screen - User can update info

        This screen lets the guest(user) modify their existing reservation details/info

        Can modify:
            - Check-In Date
            - Check-Out Date
            - Name
            - Email
            - Phone Number
            - Card Number
        """
        #Update screen with new menu display
        self.updateScreen(bColor="lemon chiffon", xSize = 0, ySize = 0)

        tk.Label(self.current_frame, text = "Modify Your Reservation", font = ("Georgia", 22, "bold"), bg = "lemon chiffon").pack(pady=10)

        #Current Booking
        #tk.Label(self.current_frame, text=" \U0001F3E8 Hotel Enigma", 
        #font=("Georgia", 30, "bold"), bg="lemon chiffon").pack(pady=30)
        #tk.Label(self.current_frame, text="Take your first step with us", 
        #font=("Lucida Handwriting", 18, "bold"), bg="lemon chiffon").pack(pady=10)
        
        old_frame = tk.LabelFrame(self.current_frame, padx = 10, pady = 10, bg = "#023553")
        old_frame.pack(fill="x", pady = 10)
        old_frame_label = tk.Label(old_frame, text="Current Reservation:", font=("Times New Roman", 20, "italic", "bold"), bg="#023553", fg="lemon chiffon")
        old_frame_label.pack(side="top", anchor = "center")

        tk.Label(old_frame, text=f"Room: {old_booking['room_type']}\n"
                 f"Check-In Date: {old_booking['check_in']}\n"
                 f"Check-Out Date: {old_booking['check_out']}\n"
                 f"Total: ${old_booking['total_price']}",
                 font = ("Times New Roman", 14, "bold"), fg = "lemon chiffon", bg="#023553").pack(anchor = "center")
        
        #New Dates
        new_frame = tk.LabelFrame(self.current_frame, bg = "#023553", padx = 10, pady = 10)
        new_frame.pack(fill="x",pady=10)
        new_frame_label = tk.Label(new_frame, text="New Dates", font=("Times New Roman", 20, "italic", "bold"), bg="#023553", fg="lemon chiffon")
        new_frame_label.pack(side="top", anchor = "center")

        tk.Label(new_frame, text="Check-In Date:", font = ("Times New Roman", 14, "bold"), fg = "lemon chiffon", bg = "#023553").pack()
        check_in_entry = tk.Entry(new_frame, width=20)
        check_in_entry.pack()
        check_in_entry.insert(0, (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))

        tk.Label(new_frame, text="Check-Out Date:", font = ("Times New Roman", 14, "bold"), fg = "lemon chiffon", bg = "#023553").pack()
        check_out_entry = tk.Entry(new_frame, width=20)
        check_out_entry.pack()
        check_out_entry.insert(0, (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))

        #Guest Info
        guest_frame = tk.LabelFrame(self.current_frame, bg="#023553", padx=10, pady=10)
        guest_frame.pack(fill="x",pady=10)
        guest_frame_label = tk.Label(guest_frame, text="Guest Information", font=("Times New Roman", 20, "italic", "bold"), bg="#023553", fg="lemon chiffon")
        guest_frame_label.pack(side="top", anchor = "center")

        tk.Label(guest_frame, text="Name:", font = ("Times New Roman", 14, "bold"), fg = "lemon chiffon", bg = "#023553").pack()
        name_entry = tk.Entry(guest_frame, width=30)
        name_entry.pack()
        name_entry.insert(0, old_booking['guest_name'])

        tk.Label(guest_frame, text="Email:", font = ("Times New Roman", 14, "bold"), fg = "lemon chiffon", bg = "#023553", pady=10).pack()
        email_entry = tk.Entry(guest_frame, width=30)
        email_entry.pack()
        email_entry.insert(0, old_booking['guest_email'])

        tk.Label(guest_frame, text="Phone #:", font = ("Times New Roman", 14, "bold"), fg = "lemon chiffon", bg = "#023553", pady=10).pack()
        phone_entry = tk.Entry(guest_frame, width=20)
        phone_entry.pack()
        phone_entry.insert(0, old_booking['guest_phone'])

        tk.Label(guest_frame, text="Card #:", font = ("Times New Roman", 14, "bold"), fg = "lemon chiffon", bg = "#023553", pady=10).pack()
        card_entry = tk.Entry(guest_frame, width=20)
        card_entry.pack()

        def save_changes():
            """
            Save Reservation Changes
            
            Validates if changes enter are appropiate values
            """
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
                'check_out': check_out,
                'nights': nights
            }

            modify_reservation(old_conf, new_guest_info, new_prefs, room, self.email_sender, self.email_password)
            messagebox.showinfo("SUCCESS", "Reservation Updated!")
            self.show_homepage()

        # Buttons
        self.createButton(buttonText="Save Changes",color="green",toDo=save_changes,space=15,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=self.show_homepage,space=0,size=12)
        
    #Cancel stuff
    def show_cancel(self):
        """
        Cancel Reservation Menu

        Here the user will be prompted to enter their confirmation
        number to make sure the reservation exists

        If it exists they will proceed to the next step in the cancellation process
        """
        self.updateScreen(bColor="lemon chiffon", xSize = 0, ySize = 0)

        tk.Label(self.current_frame, text="Cancel Reservation", bg=("lemon chiffon"), font=("Georgia", 22, "bold")).pack(pady=20)
        tk.Label(self.current_frame, text="Confirmation Number:", bg=("lemon chiffon"), font=("Helvetica", 12, "bold")).pack()

        conf_entry = tk.Entry(self.current_frame, width=30, font=("Times New Roman",12))
        conf_entry.pack(pady=10)
        method=self.confirm_cancel

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "imageResources", "mainpage.png")
        image = Image.open(image_path)
        image = image.resize((500, 400), Image.LANCZOS)  # Resize image to fit
        rounded_image = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image)
        image_label = tk.Label(self.current_frame, image=photo, bg="lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x=60, y=300)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path2 = os.path.join(BASE_DIR, "imageResources", "contactus.webp")
        image = Image.open(image_path2)
        image = image.resize((500, 300), Image.LANCZOS)  # Resize image to fit
        rounded_image2 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image2)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 970, y = 350)        

        # Buttons
        self.createButton(buttonText="Search",color="#023553",toDo=lambda: self.search(conf_entry,method),space=10,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=self.show_homepage,space=0,size=12)

    def confirm_cancel(self,conf_num, booking):
        """
        Cancel Reservation Menu

        Here the User will be prompted whether the want to confirm a cancellation
        of the reservation or if they would rather keep the reservation
        """
        # Update screen with new menu display
        self.updateScreen(bColor="lightyellow", xSize = 0, ySize = 0)
        tk.Label(self.current_frame, text="Confirm Cancellation",font=("Times New Roman",16,"bold"),
                 bg="lightyellow").pack(pady=10)
        info_frame = tk.LabelFrame(self.current_frame, text = "Reservation", padx= 10, pady = 10,bg = "lightyellow")
        info_frame.pack(fill="x", pady=10)

        tk.Label(info_frame, text=f"Confirmation: {conf_num}\n"
                 f"Guest: {booking['guest_name']}\n"
                 f"Room: {booking['room_type']}\n"
                 f"Check-in: {booking['check_in']}\n"
                 f"Total: ${booking['total_price']}", bg="lightyellow").pack(anchor="w")

        def cancel():
            """Cancel Reservation: cancels the users reservation"""
            cancel_reservation(conf_num, booking, self.email_sender, self.email_password)
            messagebox.showinfo("SUCCESS", "Reservation Cancelled!")
            self.show_homepage()

        # Buttons
        self.createButton(buttonText="Confirm Cancellation",color="red",toDo=cancel,space=20,size=12)
        self.createButton(buttonText="Keep Reservation",color="green",toDo=self.show_homepage,space=0,size=12)
        
    #Report
    def show_login(self):
        """
        Show Admin Login Screen
        
        Will verify if user is an Admin, if so they will proceed 
        to be able to view hotel report
        """
        # Update screen with new menu display
        self.updateScreen(bColor="lemon chiffon",xSize=0,ySize=0)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path2 = os.path.join(BASE_DIR, "imageResources", "reportAdminBlue.png")
        image = Image.open(image_path2)
        image = image.resize((250, 250), Image.LANCZOS)  # Resize image to fit
        rounded_image2 = self.create_rounded_image(image, 30)
        photo = ImageTk.PhotoImage(rounded_image2)
        image_label = tk.Label(self.current_frame, image = photo, bg = "lemon chiffon")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.place(x = 655, y = 400)

        tk.Label(self.current_frame, text="Admin Login", bg=("lemon chiffon"), font=("Georgia", 22, "bold")).pack(pady=20)
        tk.Label(self.current_frame, text="Username:", bg=("lemon chiffon"), font=("Helvetica", 12, "bold")).pack(pady=5)
        user_entry = tk.Entry(self.current_frame, width=30)
        user_entry.pack()
        tk.Label(self.current_frame, text="Password:", bg=("lemon chiffon"), font=("Helvetica", 12, "bold")).pack(pady=5)
        pass_entry = tk.Entry(self.current_frame, width=30, show="*")
        pass_entry.pack()

        #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        #image_path = os.path.join(BASE_DIR, "imageResources", "mainpage.png")
        #image = Image.open(image_path)
        #image = image.resize((500, 400), Image.LANCZOS)  #Resize image to fit
        #rounded_image = self.create_rounded_image(image, 30)
        #photo = ImageTk.PhotoImage(rounded_image)
        #image_label = tk.Label(self.current_frame, image=photo, bg="lemon chiffon")
        #image_label.image = photo  #Keep a reference to avoid garbage collection
        #image_label.place(x=60, y=300)        

        def login():
            """Verifies Employee Login: sees if user is an employee"""
            if user_entry.get() == self.admin_user and pass_entry.get() == self.admin_pass:
                self.show_report_options()
            else:
                messagebox.showerror("ERROR", "Invalid Credentials")
        
        # Buttons
        self.createButton(buttonText="Login", color="#023553", toDo=login, space=20, size=12)
        self.createButton(buttonText="Back", color="gray", toDo=self.show_homepage, space=0,size=12)

    def show_report_options(self):
        """
        Displays Hotel Report Options to Admin

        Allows admin to generate a report of all reservations or generate
        a report for reservations of a certain date range
        """
        # Update screen with new menu display
        self.updateScreen(bColor = "lemon chiffon", xSize = 0, ySize = 0)

        tk.Label(self.current_frame, text="Report Options", font=("Georgia", 22, "bold"), bg = "lemon chiffon").pack(pady=20)
        report_type = tk.StringVar(value="all")
        tk.Radiobutton(self.current_frame, text="All Reservations", font = ("Times New Roman", 12, "bold"), bg = "lemon chiffon", variable=report_type,
                       value="all").pack(anchor = "center", padx = 20, pady = 5)
        tk.Radiobutton(self.current_frame, text="Custom Date Range", font = ("Times New Roman", 12, "bold"), bg = "lemon chiffon", variable=report_type,
                       value="custom").pack(anchor = "center", padx = 20, pady = 5)
        
        date_frame = tk.LabelFrame(self.current_frame, padx = 10, pady = 10, bg ="#023553")
        date_frame.pack(fill="x", padx=20, pady=10)
        data_label = tk.Label(date_frame, text="Reservation Dates:", font=("Times New Roman", 20, "italic", "bold"), bg="#023553", fg="lemon chiffon")
        data_label.pack(side="top", anchor = "center")

        tk.Label(date_frame, text="Start Date:", font = ("Times New Roman", 12, "bold"), fg = "lemon chiffon", bg= "#023553").pack()
        start_entry = tk.Entry(date_frame, width=20)
        start_entry.pack()
        start_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        tk.Label(date_frame, text="End Date:", font = ("Times New Roman", 12, "bold"), fg = "lemon chiffon" ,bg = "#023553", pady=10).pack()
        end_entry = tk.Entry(date_frame, width=20)
        end_entry.pack()
        end_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def generate():
            """
            Creates a hotel report for admin
            
            If admin selects custom verifies dates are appropiate values
            """
            bookings = load_bookings()
            if report_type.get() == "custom":
                start = validate_date(start_entry.get())
                end = validate_date(end_entry.get())
                if not start or not end:
                    messagebox.showerror("ERROR", "Invalid Dates")
                    return
                bookings = [b for b in bookings
                            if start <= validate_date(b['check_in']) <= end]

            self.show_report(bookings)

        # Buttons
        self.createButton(buttonText="Generate",color="green",toDo=generate,space=20,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=self.show_homepage,space=0,size=12)

    def show_report(self, bookings):
        """
        Displays Hotel Report for admin: allows admin to save report or
        go back to homepage(main menu)
        """
        # Update screen with new menu display
        self.updateScreen(bColor="lemon chiffon",xSize=20,ySize=20)
        tk.Label(self.current_frame, text="Hotel Reservation Report", font=("Times New Roman", 18, "bold")).pack(pady=10)
        # Calculate Statistics
        total_revenue = sum(b.get('total_price', 0) for b in bookings
                            if b.get('status') == 'CONFIRMED')
        confirmed = sum(1 for b in bookings if b.get('status') == 'CONFIRMED')
        cancelled = sum(1 for b in bookings if b.get('status') == 'CANCELLED')
        # Create Report Text
        report = f"""Hotel Reservation Report
{'='*50}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

SUMMARY:
Total Reservations: {len(bookings)}
Confirmed Reservations: {confirmed}
Cancelled Reservations: {cancelled}
Total Revenue: ${total_revenue:.2f}
Average Value: ${total_revenue/confirmed if confirmed > 0 else 0:.2f}

{'='*50}
DETAILS:
"""
        for b in bookings: 
            report += f"""   
Confirmation #: {b.get('confirmation_number')}
Guest: {b.get('guest_name')}
Email: {b.get('guest_email')}
Room: {b.get('room_type')}
Check-In Date: {b.get('check_in')}
Check-Out Date: {b.get('check_out')}
Total: ${b.get('total_price')}
Status: {b.get('status')}
{'-'*50}"""
            
        # Display in Scrolled Text
        text_area = scrolledtext.ScrolledText(self.current_frame, width=80,height=20,font=("Courier",9))
        text_area.pack(pady=10, fill="both", expand=True)
        text_area.insert(tk.END, report)
        text_area.config(state=tk.DISABLED)

        def save():
            """Saves Admin Generated Report"""
            filename = f"report_{datetime.now().strftime('%y%m%d_%H%M%S')}.txt"
            try:
                with open(filename, 'w') as f:
                    f.write(report)
                messagebox.showinfo("SUCCESS", f"Saved: {filename}")
            except:
                messagebox.showerror("ERROR", "Could Not Save Report")
            
        # Buttons
        self.createButton(buttonText="Save Report",color="green",toDo=save,space=10,size=12)
        self.createButton(buttonText="Back",color="gray",toDo=self.show_homepage,space=0,size=12)
