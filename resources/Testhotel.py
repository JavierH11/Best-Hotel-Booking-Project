import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk

class ReservationFormScreen:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Reservation Form Screen")
        self.create_widgets()

    def create_widgets(self):
        self.date_label = tk.Label(self.root, text="Select Your Check-in Date:", font=('Times New Roman', 14))
        self.date_label.pack(pady=1, padx=1)
        self.calendar = Calendar(self.root)
        self.calendar.pack(pady=10, padx=10)
        self.room_label = tk.Label(self.root, text="Select Room Type:", font=('Times New Roman', 14))
        self.room_label.pack(pady=10)
        self.room_type = ttk.Combobox(self.root, values=["Single Room", "Double Room", "Junior Room", "Family Room", "Suite", "Honeymoon Suite", "Penthouse Suite", "Presidential Suite"])
        self.room_type.pack(pady=10)
        self.amenities_label = tk.Label(self.root, text="Additional Amenities:", font=('Times New Roman', 14))
        self.amenities_label.pack(pady=10, anchor=tk.W)

        self.amenities_vars = []
        for amenity in ["Wi-Fi", "Breakfast", "Pool Access", "Restock Mini-Fridge"]:
            var = tk.BooleanVar()
            self.amenities_vars.append(var)
            cb = tk.Checkbutton(self.root, text=amenity, variable=var)
            cb.pack(anchor=tk.W)
        self.submit_button = tk.Button(self.root, font=('Times New Roman', 16), text="Reserve", command=self.reserve, width=10)
        self.submit_button.pack(pady=20)

    def reserve(self):
        selected_date = self.calendar.get_date()
        selected_room = self.room_type.get()
        selected_amenities = [amenity for var, amenity in zip(self.amenities_vars, ["Wi-Fi", "Breakfast", "Pool Access", "Restock Mini-Fridge"]) if var.get()]
        self.save_reservation(selected_room, selected_date, selected_amenities)
        self.open_confirmation_screen(selected_room, selected_date, selected_amenities)

    def save_reservation(self, room, date, amenities):
        with open("reservation.txt", "w") as file:
            file.write(f"Room: {room}\n")
            file.write(f"Date: {date}\n")
            file.write("Amenities: " + ", ".join(amenities) + "\n")

    def open_confirmation_screen(self, room, date, amenities):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.geometry(f"{screen_width}x{screen_height}+0+0")
        confirmation_label = tk.Label(self.new_window, text=f"Reservation made for '{room}' on '{date}' with the following additional amenities: {', '.join(amenities)}", font=('Times New Roman', 16))
        confirmation_label.pack(pady=20)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    image = Image.open("C:\\Users\\colle\\OneDrive\\Documents\\Comp 380\\GroupProj\\Borat-Thumbs-Up-Excited-meme-6.jpg")
    photo = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    gui = ReservationFormScreen(root)
    root.mainloop()