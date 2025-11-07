# controllers.py
"""
Hotel Booking System - Controllers
Business logic layer for managing operations
"""
from models import *
from typing import List, Optional
import json

class ReservationController:
    def __init__(self):
        self.reservations: List[Reservation] = []
    
    def create_reservation(self, reservation_id: str, user_id: str, room_id: str, 
                          check_in: str, check_out: str) -> Reservation:
        reservation = Reservation(reservation_id, user_id, room_id, check_in, check_out)
        self.reservations.append(reservation)
        return reservation
    
    def modify_reservation(self, reservation_id: str, check_in: str = None, check_out: str = None) -> bool:
        for res in self.reservations:
            if res.reservation_id == reservation_id:
                if check_in:
                    res.check_in = check_in
                if check_out:
                    res.check_out = check_out
                return True
        return False
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        for res in self.reservations:
            if res.reservation_id == reservation_id:
                res.cancel()
                return True
        return False
    
    def confirm_reservation(self, reservation_id: str) -> bool:
        for res in self.reservations:
            if res.reservation_id == reservation_id:
                res.confirm()
                return True
        return False
    
    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        for res in self.reservations:
            if res.reservation_id == reservation_id:
                return res
        return None

class PaymentController:
    def __init__(self):
        self.payments: List[Payment] = []
    
    def process_payment(self, payment_id: str, reservation_id: str, amount: float, method: str) -> Payment:
        payment = Payment(payment_id, reservation_id, amount, method)
        payment.process()
        self.payments.append(payment)
        return payment
    
    def refund_payment(self, payment_id: str) -> bool:
        for payment in self.payments:
            if payment.payment_id == payment_id:
                return payment.refund()
        return False
    
    def get_payment_details(self, payment_id: str) -> Optional[dict]:
        for payment in self.payments:
            if payment.payment_id == payment_id:
                return payment.get_payment_details()
        return None

class RoomController:
    def __init__(self):
        self.rooms: List[Room] = []
    
    def add_room(self, room_id: str, room_type: str, max_occupancy: int, price: float) -> Room:
        room = Room(room_id, room_type, max_occupancy, price)
        self.rooms.append(room)
        return room
    
    def get_room(self, room_id: str) -> Optional[Room]:
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        return None
    
    def get_available_rooms(self, check_in: str, check_out: str) -> List[Room]:
        available = []
        for room in self.rooms:
            # Check if room is available for dates
            available.append(room)
        return available
    
    def get_all_rooms(self) -> List[Room]:
        return self.rooms

class CalendarController:
    def __init__(self):
        self.calendars: dict = {}  # room_id -> Calendar
    
    def create_calendar(self, room_id: str):
        calendar_id = f"CAL_{room_id}"
        self.calendars[room_id] = Calendar(calendar_id, room_id)
    
    def mark_available(self, room_id: str, date: str):
        if room_id in self.calendars:
            self.calendars[room_id].mark_available(date)
    
    def mark_unavailable(self, room_id: str, date: str):
        if room_id in self.calendars:
            self.calendars[room_id].mark_unavailable(date)
    
    def is_date_available(self, room_id: str, date: str) -> bool:
        if room_id in self.calendars:
            return self.calendars[room_id].is_available(date)
        return False

class UserController:
    def __init__(self):
        self.users: List[User] = []
    
    def register_user(self, user_id: str, name: str, email: str, password: str) -> User:
        user = User(user_id, name, email, password)
        self.users.append(user)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def authenticate_user(self, user_id: str, password: str) -> bool:
        user = self.get_user(user_id)
        if user and user.password == password:
            return True
        return False

class ReportController:
    def __init__(self):
        self.reports: List[Report] = []
    
    def generate_booking_report(self) -> Report:
        report = Report(f"REP_{len(self.reports)}", "Booking Summary")
        self.reports.append(report)
        return report
    
    def generate_payment_report(self) -> Report:
        report = Report(f"REP_{len(self.reports)}", "Payment Summary")
        self.reports.append(report)
        return report
    
    def get_report(self, report_id: str) -> Optional[Report]:
        for report in self.reports:
            if report.report_id == report_id:
                return report
        return None
