# models.py
"""
Hotel Booking System - Data Models
All classes representing the core entities
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

# Enums
class ReservationType(Enum):
    SINGLE = "Single"
    DOUBLE = "Double"
    SUITE = "Suite"

class ReservationStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

# Core Model Classes
class Amenity:
    def __init__(self, amenity_id: str, amenity_type: str):
        self.amenity_id = amenity_id
        self.amenity_type = amenity_type
    
    def get_amenity_details(self) -> str:
        return f"Amenity: {self.amenity_type}"

class Room:
    def __init__(self, room_id: str, room_type: str, max_occupancy: int, price: float):
        self.room_id = room_id
        self.room_type = room_type
        self.max_occupancy = max_occupancy
        self.price = price
        self.amenities: List[Amenity] = []
    
    def add_amenity(self, amenity: Amenity):
        self.amenities.append(amenity)
    
    def get_room_details(self) -> dict:
        return {
            "room_id": self.room_id,
            "room_type": self.room_type,
            "max_occupancy": self.max_occupancy,
            "price": self.price,
            "amenities": [a.amenity_type for a in self.amenities]
        }

class Calendar:
    def __init__(self, calendar_id: str, room_id: str):
        self.calendar_id = calendar_id
        self.room_id = room_id
        self.available_dates: dict = {}
    
    def mark_available(self, date: str):
        self.available_dates[date] = True
    
    def mark_unavailable(self, date: str):
        self.available_dates[date] = False
    
    def is_available(self, date: str) -> bool:
        return self.available_dates.get(date, False)

class User:
    def __init__(self, user_id: str, name: str, email: str, password: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
    
    def get_user_details(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }

class Reservation:
    def __init__(self, reservation_id: str, user_id: str, room_id: str, 
                 check_in: str, check_out: str):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = ReservationStatus.PENDING
        self.created_at = datetime.now().isoformat()
    
    def confirm(self):
        self.status = ReservationStatus.CONFIRMED
    
    def cancel(self):
        self.status = ReservationStatus.CANCELLED
    
    def complete(self):
        self.status = ReservationStatus.COMPLETED
    
    def get_reservation_details(self) -> dict:
        return {
            "reservation_id": self.reservation_id,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "status": self.status.value
        }

class Payment:
    def __init__(self, payment_id: str, reservation_id: str, amount: float, method: str):
        self.payment_id = payment_id
        self.reservation_id = reservation_id
        self.amount = amount
        self.payment_method = method
        self.status = PaymentStatus.PENDING
        self.payment_date = None
    
    def process(self) -> bool:
        self.status = PaymentStatus.COMPLETED
        self.payment_date = datetime.now().isoformat()
        return True
    
    def refund(self) -> bool:
        self.status = PaymentStatus.REFUNDED
        return True
    
    def get_payment_details(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "status": self.status.value,
            "payment_date": self.payment_date
        }

class Report:
    def __init__(self, report_id: str, report_type: str):
        self.report_id = report_id
        self.report_type = report_type
        self.generated_date = datetime.now().isoformat()
    
    def generate(self) -> dict:
        return {
            "report_id": self.report_id,
            "type": self.report_type,
            "generated": self.generated_date
        }
