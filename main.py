# main.py
"""
Hotel Booking System - Main Application
Entry point and system orchestration
"""
from models import *
from controllers import *

class HotelBookingSystem:
    def __init__(self):
        self.reservation_controller = ReservationController()
        self.payment_controller = PaymentController()
        self.room_controller = RoomController()
        self.calendar_controller = CalendarController()
        self.user_controller = UserController()
        self.report_controller = ReportController()
    
    # User Management
    def register_user(self, user_id: str, name: str, email: str, password: str):
        return self.user_controller.register_user(user_id, name, email, password)
    
    def authenticate(self, user_id: str, password: str) -> bool:
        return self.user_controller.authenticate_user(user_id, password)
    
    # Room Management
    def add_room(self, room_id: str, room_type: str, max_occupancy: int, price: float):
        room = self.room_controller.add_room(room_id, room_type, max_occupancy, price)
        self.calendar_controller.create_calendar(room_id)
        return room
    
    def get_available_rooms(self, check_in: str, check_out: str) -> List[Room]:
        return self.room_controller.get_available_rooms(check_in, check_out)
    
    def add_amenity_to_room(self, room_id: str, amenity_id: str, amenity_type: str):
        room = self.room_controller.get_room(room_id)
        if room:
            amenity = Amenity(amenity_id, amenity_type)
            room.add_amenity(amenity)
            return True
        return False
    
    # Reservation Management
    def create_reservation(self, reservation_id: str, user_id: str, room_id: str, 
                          check_in: str, check_out: str) -> Optional[Reservation]:
        # Check if user exists
        if not self.user_controller.get_user(user_id):
            return None
        
        # Check if room exists
        if not self.room_controller.get_room(room_id):
            return None
        
        return self.reservation_controller.create_reservation(
            reservation_id, user_id, room_id, check_in, check_out
        )
    
    def modify_reservation(self, reservation_id: str, check_in: str = None, check_out: str = None) -> bool:
        return self.reservation_controller.modify_reservation(reservation_id, check_in, check_out)
    
    def confirm_reservation(self, reservation_id: str) -> bool:
        return self.reservation_controller.confirm_reservation(reservation_id)
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        return self.reservation_controller.cancel_reservation(reservation_id)
    
    # Payment Management
    def process_payment(self, payment_id: str, reservation_id: str, amount: float, method: str):
        return self.payment_controller.process_payment(payment_id, reservation_id, amount, method)
    
    def refund_payment(self, payment_id: str) -> bool:
        return self.payment_controller.refund_payment(payment_id)
    
    # Calendar Management
    def mark_date_available(self, room_id: str, date: str):
        self.calendar_controller.mark_available(room_id, date)
    
    def mark_date_unavailable(self, room_id: str, date: str):
        self.calendar_controller.mark_unavailable(room_id, date)
    
    def check_availability(self, room_id: str, date: str) -> bool:
        return self.calendar_controller.is_date_available(room_id, date)
    
    # Reporting
    def generate_booking_report(self):
        return self.report_controller.generate_booking_report()
    
    def generate_payment_report(self):
        return self.report_controller.generate_payment_report()


# Example Usage
if __name__ == "__main__":
    system = HotelBookingSystem()
    
    # Register users
    system.register_user("U001", "John Doe", "john@email.com", "password123")
    system.register_user("U002", "Jane Smith", "jane@email.com", "password456")
    
    # Add rooms
    room1 = system.add_room("R001", "Single", 1, 100.0)
    room2 = system.add_room("R002", "Double", 2, 150.0)
    room3 = system.add_room("R003", "Suite", 4, 250.0)
    
    # Add amenities
    system.add_amenity_to_room("R001", "A001", "WiFi")
    system.add_amenity_to_room("R001", "A002", "Air Conditioning")
    system.add_amenity_to_room("R002", "A003", "Jacuzzi")
    system.add_amenity_to_room("R003", "A004", "Kitchen")
    
    # Mark dates as available
    for i in range(1, 31):
        date_str = f"2024-12-{i:02d}"
        system.mark_date_available("R001", date_str)
        system.mark_date_available("R002", date_str)
        system.mark_date_available("R003", date_str)
    
    # Create reservation
    res = system.create_reservation("RES001", "U001", "R001", "2024-12-10", "2024-12-12")
    if res:
        print(f"✅ Reservation created: {res.reservation_id}")
        print(f"   Details: {res.get_reservation_details()}")
    
    # Confirm reservation
    if system.confirm_reservation("RES001"):
        print("✅ Reservation confirmed")
    
    # Process payment
    payment = system.process_payment("PAY001", "RES001", 200.0, "Credit Card")
    if payment:
        print(f"✅ Payment processed: {payment.get_payment_details()}")
    
    # Generate reports
    booking_report = system.generate_booking_report()
    print(f"✅ Booking report generated: {booking_report.generate()}")
    
    print("\n🎉 Hotel Booking System is running successfully!")
