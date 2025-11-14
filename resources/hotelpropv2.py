import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import random

class HotelReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reservation System")
        self.reservations = {}
        self.create_home_screen()

    def create_home_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Hotel Reservation System", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Make a Reservation", command=self.make_reservation).pack(pady=10)
        tk.Button(self.root, text="Modify a Reservation", command=self.modify_reservation).pack(pady=10)
        tk.Button(self.root, text="Cancel a Reservation", command=self.cancel_reservation).pack(pady=10)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).pack(pady=10)

    def make_reservation(self):
        self.clear_screen()
        self.date_label = tk.Label(self.root, text="Select Date:")
        self.date_label.pack()
        self.calendar = Calendar(self.root)
        self.calendar.pack(pady=10)

        tk.Label(self.root, text="Select Room Type:").pack()
        self.room_type = ttk.Combobox(self.root, values=["Single - $100", "Double - $150", "Suite - $200"])
        self.room_type.pack(pady=10)

        tk.Label(self.root, text="Select Amenities:").pack()
        self.amenities = ttk.Combobox(self.root, values=["WiFi - $10", "Breakfast - $20", "Parking - $15"])
        self.amenities.pack(pady=10)

        tk.Button(self.root, text="Confirm Reservation", command=self.confirm_reservation).pack(pady=20)

    def confirm_reservation(self):
        date = self.calendar.get_date()
        room = self.room_type.get()
        amenities = self.amenities.get()
        confirmation_number = random.randint(1000, 9999)

        self.reservations[confirmation_number] = {
            "date": date,
            "room": room,
            "amenities": amenities
        }

        summary = f"Reservation Confirmed!\nDate: {date}\nRoom: {room}\nAmenities: {amenities}\nConfirmation Number: {confirmation_number}"
        messagebox.showinfo("Reservation Summary", summary)
        self.create_home_screen()

    def modify_reservation(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Confirmation Number:").pack()
        self.confirmation_entry = tk.Entry(self.root)
        self.confirmation_entry.pack(pady=10)
        tk.Button(self.root, text="Fetch Reservation", command=self.fetch_reservation).pack(pady=20)

    def fetch_reservation(self):
        confirmation_number = int(self.confirmation_entry.get())
        if confirmation_number in self.reservations:
            self.make_reservation()
            reservation = self.reservations[confirmation_number]
            self.calendar.set_date(reservation["date"])
            self.room_type.set(reservation["room"])
            self.amenities.set(reservation["amenities"])
            tk.Button(self.root, text="Update Reservation", command=lambda: self.update_reservation(confirmation_number)).pack(pady=20)
        else:
            messagebox.showerror("Error", "Reservation not found.")

    def update_reservation(self, confirmation_number):
        self.confirm_reservation()

    def cancel_reservation(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Confirmation Number:").pack()
        self.confirmation_entry = tk.Entry(self.root)
        self.confirmation_entry.pack(pady=10)
        tk.Button(self.root, text="Cancel Reservation", command=self.process_cancellation).pack(pady=20)

    def process_cancellation(self):
        confirmation_number = int(self.confirmation_entry.get())
        if confirmation_number in self.reservations:
            del self.reservations[confirmation_number]
            messagebox.showinfo("Cancellation", "Reservation has been cancelled. Refund will be processed in 7 business days.")
            self.create_home_screen()
        else:
            messagebox.showerror("Error", "Reservation not found.")

    def generate_report(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Manager Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)
        tk.Button(self.root, text="Submit", command=self.check_password).pack(pady=20)

    def check_password(self):
        if self.password_entry.get() == "test":
            report = "\n".join([f"Confirmation: {k}, Details: {v}" for k, v in self.reservations.items()])
            messagebox.showinfo("Reservations Report", report if report else "No reservations found.")
            self.create_home_screen()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelReservationApp(root)
    root.mainloop()