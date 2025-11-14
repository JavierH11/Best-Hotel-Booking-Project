import tkinter as tk
from tkinter import ttk

# GUI set up
reservationSS = tk.Tk()
reservationSS.title("Reservation Summary Screen")
reservationSS.geometry("800x1200")
reservationSS.config(background = "white")

# Title of the ReservationScreenSummary GUI
label = tk.Label(reservationSS,
    text = "Your Reservation Summary!",
    font = ('Arial', 40, 'bold'),
    fg = 'black',
    bg = 'white')
label.pack(pady = 10)

# Reservation Summary Contents
contents = tk.Frame(reservationSS, bg = "white", highlightbackground = "#cccccc", highlightthickness = 2)
contents.pack(fill = "both", expand = True, padx = 40, pady = 10)
contents.grid_columnconfigure(1, weight = 1)

guestNameVar = tk.StringVar(value = "Brad Gordon")  # dummy Var
guestNameLabel = tk.Label(contents, text = "Guest Name:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
guestNameValue = tk.Label(contents, textvariable = guestNameVar, font = ('Arial', 14), bg = "white", fg = "black")
guestNameLabel.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 6)
guestNameValue.grid(row = 0, column = 1, sticky = "w", padx = 10, pady = 6)

reservationIDvar = tk.StringVar(value = "ABC12345")  # dummy Var
reservationIdLabel = tk.Label(contents, text = "Reservation ID:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
reservationIdValue = tk.Label(contents, textvariable = reservationIDvar, font = ('Arial', 14), bg = "white", fg = "black")
reservationIdLabel.grid(row = 1, column = 0, sticky = "w", padx = 10, pady = 6)
reservationIdValue.grid(row = 1, column = 1, sticky = "w", padx = 10, pady = 6)

checkInVar = tk.StringVar(value = "12/24/2025")  # dummy Var
checkInLabel = tk.Label(contents, text = "Check-In Date:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
checkInValue = tk.Label(contents, textvariable = checkInVar, font = ('Arial', 14), bg = "white", fg = "black")
checkInLabel.grid(row = 2, column = 0, sticky = "w", padx = 10, pady = 6)
checkInValue.grid(row = 2, column = 1, sticky = "w", padx = 10, pady = 6)

checkOutVar = tk.StringVar(value = "01/06/2026")  # dummy Var
checkOutLabel = tk.Label(contents, text = "Check-Out Date:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
checkOutValue = tk.Label(contents, textvariable = checkOutVar, font = ('Arial', 14), bg = "white", fg = "black")
checkOutLabel.grid(row = 3, column = 0, sticky = "w", padx = 10, pady = 6)
checkOutValue.grid(row = 3, column = 1, sticky = "w", padx = 10, pady = 6)

numOfNightsVar = tk.StringVar(value = "13")  # dummy Var
numOfNightsLabel = tk.Label(contents, text = "Number of Nights:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
numOfNightsValue = tk.Label(contents, textvariable = numOfNightsVar, font = ('Arial', 14), bg = "white", fg = "black")
numOfNightsLabel.grid(row = 4, column = 0, sticky = "w", padx = 10, pady = 6)
numOfNightsValue.grid(row = 4, column = 1, sticky = "w", padx = 10, pady = 6)

guestNumVar = tk.StringVar(value = "2 Adults, 1 Child")  # dummy Var
guestNumLabel = tk.Label(contents, text = "Number of Guests:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
guestNumValue = tk.Label(contents, textvariable = guestNumVar, font = ('Arial', 14), bg = "white", fg = "black")
guestNumLabel.grid(row = 5, column = 0, sticky = "w", padx = 10, pady = 6)
guestNumValue.grid(row = 5, column = 1, sticky = "w", padx = 10, pady = 6)

roomTypeVar = tk.StringVar(value = "Deluxe Suite")  # dummy Var
roomTypeLabel = tk.Label(contents, text = "Room Type:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
roomTypeValue = tk.Label(contents, textvariable = roomTypeVar, font = ('Arial', 14), bg = "white", fg = "black")
roomTypeLabel.grid(row = 6, column = 0, sticky = "w", padx = 10, pady = 6)
roomTypeValue.grid(row = 6, column = 1, sticky = "w", padx = 10, pady = 6)

pricePerNightVar = tk.StringVar(value = "$235.00 /night")  # dummy Var
pricePerNightLabel = tk.Label(contents, text = "Price per Night:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
pricePerNightValue = tk.Label(contents, textvariable = pricePerNightVar, font = ('Arial', 14), bg = "white", fg = "black")
pricePerNightLabel.grid(row = 7, column = 0, sticky = "w", padx = 10, pady = 6)
pricePerNightValue.grid(row = 7, column = 1, sticky = "w", padx = 10, pady = 6)

totalPriceVar = tk.StringVar(value = "$3055.00 /total ")  # dummy Var
totalPriceLabel = tk.Label(contents, text = "Total Price:", font = ('Arial', 14, 'bold'), bg = "white", fg = "black")
totalPriceValue = tk.Label(contents, textvariable = totalPriceVar, font = ('Arial', 14), bg = "white", fg = "black")
totalPriceLabel.grid(row = 8, column = 0, sticky = "w", padx = 10, pady = 6)
totalPriceValue.grid(row = 8, column = 1, sticky = "w", padx = 10, pady = 6)

for i in range(9):
    contents.grid_rowconfigure(i, weight = 1)


# Confirm, Cancel & Modify Buttons
bottom = tk.Frame(reservationSS, bg = "white")
bottom.pack(side = "bottom", fill = "x", pady = 30)

bottom.grid_columnconfigure(0, weight = 1)
bottom.grid_columnconfigure(1, weight = 1)
bottom.grid_columnconfigure(2, weight = 1)

confirmButton = tk.Button(bottom, 
	text = "Confirm Reservation", 
	font = ('Arial', 15), 
	bg = "white", 
	fg = "black", 
	activebackground = "#e6e6e6")

cancelButton = tk.Button(bottom,
    text = "Cancel Reservation",
    font = ('Arial', 15),
    bg = "white",
    fg = "black",
    activebackground = "#e6e6e6")

modifyButton = tk.Button(bottom,
    text = "Modify Reservation",
    font = ('Arial', 15),
    bg = "white",
    fg = "black",
    activebackground = "#e6e6e6")

cancelButton.grid(row = 0, column = 0, pady = 10, sticky = "s")
modifyButton.grid(row = 0, column = 1, pady = 10, sticky = "s")
confirmButton.grid(row = 0, column = 2, pady = 10, sticky = "s")

reservationSS.mainloop()