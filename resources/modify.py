import tkinter as tk
import os

class modify_reservation_controller:
    def createReservationSummary(lineStrings,lineStart,lineEnd):
        with open('modifySummary_file.txt', 'w', encoding = 'utf-8') as file:
            file.write("PREVIOUS SUMMARY:\n")
            #uses file information without blank spaces
            for i,line in enumerate(lineStrings,1):
                if i in range(lineStart,lineEnd):
                    copy = line.strip()
                    file.write(f"{copy}\n")
            file.write("\nUPDATED SUMMARY:")
        modify_reservation_controller.updateHotelInformation(lineStrings,lineStart,lineEnd)

    def updateHotelInformation(lineStrings,lineStart,lineEnd):
        with open("hotel_information_file.txt", "r") as file:
            lines = file.readlines()
            number = 1
            #uses actual text file so take into account blank lines: (...+3, ...+5)
            with open("hotel_information_file.txt", "w", encoding = 'utf-8') as file:
                for line in lines:
                    if number not in range(lineStart+3, lineEnd+5):
                        file.write(f"{line}")
                    number +=1
               

class modify_reservation_screen_1:
    def modify_reservation_window():
        new_win = tk.Toplevel()  # Use Toplevel for a secondary window
        new_win.title("Modify Reservation Screen 1")
        new_win.geometry("500x400")

        
        #checks if confirmation number is in hotel information file
        #if number is in txt file then hotel reservation exists
        def confirmnum_exist(confirmation_number):
            #count = 0;
            confirmation_number = confirmation_number.strip()
            try:
                with open('hotel_information_file.txt', 'r', encoding = 'utf-8') as file:

                    #text file wihtout blank lines
                    lines = [line.strip() for line in file if line.strip()]

                    #get line number that contains confirmation number in text file
                    for count, line in enumerate(lines, 1):
                        if confirmation_number in line:
                            lineNum = count
                            lineMin = lineNum-5 #start of info on text file
                            lineMax = lineNum+2 #end of info on text file
                    
                    if confirmation_number in lines:
                        print(f"\n the string '{confirmation_number}' was found in file")
                        print(f"this is the line it was found: '{lineNum}' ")
                        modify_reservation_controller.createReservationSummary(lines,lineMin, lineMax)
                    else:
                        notfound_text = tk.Label(new_win, text="ERROR: Confirmation number not found. Try again.", font = ("Times New Roman", 15)).pack(pady=20)
                        print(f"\n the string '{confirmation_number}' was not found in file")
            except FileNotFoundError:
                print("ERROR: 'hotel_information_file.txt' not found")

        #saves user input as a string to later compare with txt file
        def keyboard_enter(event):
            #label.config(text=event.widget.get())
            confirmation_number = event.widget.get()
            confirmnum_exist(confirmation_number)
        
        #Ask user to input confirmation/reservation number
        enterconf_text = tk.Label(new_win, text="Please enter your confirmation number:", font = ("Times New Roman", 15)).pack(pady=20)

        #Textbox for user to input confirmation/reservation number
        #Passes input to return_pressed method
        enter_confirmation = tk.Entry(new_win)
        enter_confirmation.bind("<Return>", keyboard_enter)
        enter_confirmation.pack(pady=10)

        #later might want to add enter button that does the same thing as keyboard enter click
        #enterconf_button = tk.Button(new_win, text="Enter", command=keyboard_enter).pack(pady=10)

        #button to close window
        tk.Button(new_win, text="Close Window", command=new_win.destroy).pack(pady=10)

        new_win.mainloop()