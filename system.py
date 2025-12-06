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

if __name__ == "__main__":
    root = tk.Tk()
    app = BestHotelBookingGroup(root)
    root.mainloop()
