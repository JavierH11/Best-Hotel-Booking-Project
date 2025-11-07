# data_persistence.py
"""
Hotel Booking System - Data Persistence
Save and load data from JSON files
"""
import json
import os
from datetime import datetime

class DataPersistence:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_reservations(self, reservations):
        """Save all reservations to JSON"""
        data = []
        for res in reservations:
            data.append(res.get_reservation_details())
        
        with open(f"{self.data_dir}/reservations.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_reservations(self):
        """Load all reservations from JSON"""
        file_path = f"{self.data_dir}/reservations.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_payments(self, payments):
        """Save all payments to JSON"""
        data = []
        for payment in payments:
            data.append(payment.get_payment_details())
        
        with open(f"{self.data_dir}/payments.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_payments(self):
        """Load all payments from JSON"""
        file_path = f"{self.data_dir}/payments.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_rooms(self, rooms):
        """Save all rooms to JSON"""
        data = []
        for room in rooms:
            data.append(room.get_room_details())
        
        with open(f"{self.data_dir}/rooms.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_users(self, users):
        """Save all users to JSON"""
        data = []
        for user in users:
            data.append(user.get_user_details())
        
        with open(f"{self.data_dir}/users.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_users(self):
        """Load all users from JSON"""
        file_path = f"{self.data_dir}/users.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    
    def export_report(self, report_type="all"):
        """Export a comprehensive report"""
        report = "HOTEL BOOKING SYSTEM - MANAGEMENT REPORT\n"
        report += "=" * 70 + "\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Reservations summary
        report += "RESERVATION SUMMARY\n"
        report += "-" * 70 + "\n"
        
        reservations = self.load_reservations()
        if reservations:
            report += f"Total Reservations: {len(reservations)}\n\n"
            for res in reservations:
                report += f"Reservation ID: {res.get('reservation_id', 'N/A')}\n"
                report += f"  User: {res.get('user_id', 'N/A')}\n"
                report += f"  Room: {res.get('room_id', 'N/A')}\n"
                report += f"  Check-in: {res.get('check_in', 'N/A')}\n"
                report += f"  Check-out: {res.get('check_out', 'N/A')}\n"
                report += f"  Status: {res.get('status', 'N/A')}\n\n"
        else:
            report += "No reservations found.\n\n"
        
        # Payments summary
        report += "PAYMENT SUMMARY\n"
        report += "-" * 70 + "\n"
        
        payments = self.load_payments()
        if payments:
            total_revenue = 0
            report += f"Total Payments: {len(payments)}\n\n"
            for payment in payments:
                amount = payment.get('amount', 0)
                total_revenue += amount
                report += f"Payment ID: {payment.get('payment_id', 'N/A')}\n"
                report += f"  Amount: ${amount}\n"
                report += f"  Status: {payment.get('status', 'N/A')}\n"
                report += f"  Method: {payment.get('payment_method', 'N/A')}\n\n"
            
            report += f"\nTOTAL REVENUE: ${total_revenue}\n\n"
        else:
            report += "No payments found.\n\n"
        
        # Room occupancy
        report += "ROOM INFORMATION\n"
        report += "-" * 70 + "\n"
        
        report += "Available Rooms:\n"
        rooms = self.load_rooms()
        if rooms:
            for room in rooms:
                report += f"  {room.get('room_id')}: {room.get('room_type')} - ${room.get('price')}/night\n"
        
        return report
    
    def save_report_to_file(self, report_content, filename=None):
        """Save report to file"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            f.write(report_content)
        
        return filepath
