import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

class Room:
    def __init__(self, room_type, price):
        self.room_type = room_type
        self.price = price

class Reservation:
    def __init__(self, date, room, amenities):
        self.date = date
        self.room = room
        self.amenities = amenities

class ReservationController:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Room Reservation")
        self.create_widgets()

    def create_widgets(self):
        self.calendar = Calendar(self.root)
        self.calendar.pack(pady=10)
        self.room_label = tk.Label(self.root, text="Select Room Type:")
        self.room_label.pack()
        self.room_var = tk.StringVar()
        self.room_options = [
            Room("$100 - Single", 100),
            Room("$150 - Double", 150),
            Room("$250 - Suite", 250),
            Room("$300 - Deluxe", 300),
            Room("$200 - Family", 200),
            Room("$500 - Presidential", 500),
            Room("$80  - Economy", 80),
            Room("$120 - Standard", 120),
            Room("$400 - Luxury", 400),
            Room("$600 - Penthouse", 600)
        ]
        self.room_menu = ttk.Combobox(self.root, textvariable = self.room_var)
        self.room_menu['values'] = [room.room_type for room in self.room_options]
        self.room_menu.pack(pady=10)
        self.amenities_label = tk.Label(self.root, text="Select Amenities:")
        self.amenities_label.pack()
        self.amenities_var = tk.StringVar(value="")
        self.amenities = {"Breakfast": 20, "WiFi": 10, "Parking": 15, "Pool Access": 25, "Gym Access": 15, "Spa": 50, "Airport Shuttle": 30, "Late Checkout": 40, "Early Check-in": 35,"Room Service": 20}
        self.amenity_checkboxes = {}
        for amenity, price in self.amenities.items():
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(self.root, text=f"{amenity} (+${price})", variable=var)
            checkbox.pack(anchor='w')
            self.amenity_checkboxes[amenity] = (var, price)
        self.submit_button = tk.Button(self.root, text="Create Reservation", command=self.create_reservation)
        self.submit_button.pack(pady=20)

    def create_reservation(self):
        selected_date = self.calendar.get_date()
        selected_room = self.room_var.get()
        selected_amenities = {amenity: price for amenity, (var, price) in self.amenity_checkboxes.items() if var.get()}
        room_price = next((room.price for room in self.room_options if room.room_type == selected_room), 0)
        total_price = room_price + sum(selected_amenities.values())
        reservation = Reservation(selected_date, selected_room, selected_amenities)
        
        with open("reservation_summary.txt", "a") as file:
            file.write(f"Reservation created for {reservation.date} in a {reservation.room} room with amenities {reservation.amenities}. Total Price: ${total_price}\n")
        print(f"Reservation created for {reservation.date} in a {reservation.room} room with amenities {reservation.amenities}. The Total Price: ${total_price}")

if __name__ == "__main__":
    root = tk.Tk()
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"{screen_width}x{screen_height}+0+0") #This just adjusts to the size of the screen along with screen_width + screen_height variables
    app = ReservationController(root)
    root.mainloop()
