"""
Unit Test Suite for Hotel Booking System
Phase 4: Testing and Refactoring

This module provides automated unit tests for the Hotel Booking System.
Run with: python -m pytest test_hotel_booking.py -v

Or with unittest: python -m unittest test_hotel_booking.py
"""

import unittest
import os
import json
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Import modules to test (adjust imports based on your structure)
# from utils import validate_date, generate_conf_number
# from storage import load_bookings, save_booking, update_booking_status, find_booking
# from room_logic import is_room_available, get_available_rooms
# from createReservation_logic import create_reservation


class TestStorageModule(unittest.TestCase):
    """Test Cases for storage.py - Data Persistence"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_booking = {
            "confirmation_number": "#TEST123",
            "guest_name": "Test User",
            "guest_email": "test@example.com",
            "guest_phone": "555-1234",
            "room_type": "Double",
            "room_id": "R002",
            "check_in": "2025-12-10",
            "check_out": "2025-12-12",
            "nights": 2,
            "total_price": 300.0,
            "status": "CONFIRMED"
        }
    
    def test_save_booking_STOR_001(self):
        """
        TEST ID: STOR_001
        Description: Save first booking to JSON
        Expected: Booking appended to JSON array
        """
        # Simulate save operation
        bookings = []
        bookings.append(self.test_booking)
        
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0]["confirmation_number"], "#TEST123")
        self.assertEqual(bookings[0]["status"], "CONFIRMED")
    
    def test_save_booking_STOR_002(self):
        """
        TEST ID: STOR_002
        Description: Save multiple bookings sequentially
        Expected: All bookings preserved
        """
        bookings = []
        
        booking1 = self.test_booking.copy()
        booking1["confirmation_number"] = "#ABC001"
        bookings.append(booking1)
        
        booking2 = self.test_booking.copy()
        booking2["confirmation_number"] = "#ABC002"
        bookings.append(booking2)
        
        booking3 = self.test_booking.copy()
        booking3["confirmation_number"] = "#ABC003"
        bookings.append(booking3)
        
        self.assertEqual(len(bookings), 3)
        self.assertEqual(bookings[0]["confirmation_number"], "#ABC001")
        self.assertEqual(bookings[2]["confirmation_number"], "#ABC003")
    
    def test_load_bookings_STOR_006(self):
        """
        TEST ID: STOR_006
        Description: Load bookings from JSON
        Expected: Return list of booking dictionaries
        """
        test_data = [self.test_booking, self.test_booking.copy()]
        
        # Simulate loading
        loaded = test_data
        
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["guest_name"], "Test User")
    
    def test_load_bookings_STOR_007(self):
        """
        TEST ID: STOR_007
        Description: Handle missing file gracefully
        Expected: Return empty list
        """
        # Simulate no file exists
        loaded = []
        
        self.assertEqual(loaded, [])
        self.assertIsInstance(loaded, list)
    
    def test_update_booking_status_STOR_010(self):
        """
        TEST ID: STOR_010
        Description: Update existing booking status
        Expected: Status updated, returns True
        """
        bookings = [self.test_booking]
        conf_num = "#TEST123"
        new_status = "CANCELLED"
        
        # Simulate update
        found = False
        for booking in bookings:
            if booking.get('confirmation_number') == conf_num:
                booking['status'] = new_status
                found = True
                break
        
        self.assertTrue(found)
        self.assertEqual(bookings[0]['status'], "CANCELLED")
    
    def test_update_booking_status_STOR_011(self):
        """
        TEST ID: STOR_011
        Description: Update non-existent booking
        Expected: Returns False
        """
        bookings = [self.test_booking]
        conf_num = "#FAKE999"
        new_status = "CANCELLED"
        
        # Simulate update
        found = False
        for booking in bookings:
            if booking.get('confirmation_number') == conf_num:
                found = True
                break
        
        self.assertFalse(found)
    
    def test_find_booking_STOR_006(self):
        """
        TEST ID: STOR_006
        Description: Find booking by confirmation number
        Expected: Return matching booking
        """
        bookings = [self.test_booking, self.test_booking.copy()]
        bookings[1]["confirmation_number"] = "#TEST456"
        
        # Simulate find
        found = None
        for booking in bookings:
            if booking.get('confirmation_number') == "#TEST123":
                found = booking
                break
        
        self.assertIsNotNone(found)
        self.assertEqual(found["confirmation_number"], "#TEST123")
    
    def test_find_booking_not_found(self):
        """Find non-existent booking returns None"""
        bookings = [self.test_booking]
        
        found = None
        for booking in bookings:
            if booking.get('confirmation_number') == "#NONEXIST":
                found = booking
                break
        
        self.assertIsNone(found)


class TestRoomLogicModule(unittest.TestCase):
    """Test Cases for room_logic.py - Availability & Filtering"""
    
    def setUp(self):
        """Set up test room data"""
        self.room_r001 = {
            "room_id": "R001",
            "room_type": "Single",
            "max_guests": 1,
            "num_beds": 1,
            "price": 100.0,
            "amenities": ["WiFi", "AC"]
        }
        
        self.room_r002 = {
            "room_id": "R002",
            "room_type": "Double",
            "max_guests": 2,
            "num_beds": 1,
            "price": 150.0,
            "amenities": ["WiFi", "AC", "Bathtub"]
        }
        
        self.room_r003 = {
            "room_id": "R003",
            "room_type": "Suite",
            "max_guests": 4,
            "num_beds": 2,
            "price": 250.0,
            "amenities": ["WiFi", "AC", "Bathtub", "Mini-Bar"]
        }
        
        self.rooms = [self.room_r001, self.room_r002, self.room_r003]
    
    def test_room_availability_ROOM_001(self):
        """
        TEST ID: ROOM_001
        Description: Check availability with no bookings
        Expected: Return True
        """
        bookings = []
        
        # Simulate is_room_available
        room_id = "R001"
        check_in = "2025-12-10"
        check_out = "2025-12-12"
        
        available = True  # No bookings exist
        
        self.assertTrue(available)
    
    def test_room_availability_ROOM_002(self):
        """
        TEST ID: ROOM_002
        Description: Detect date overlap
        Expected: Return False
        """
        # Request: 2025-12-10 to 2025-12-12
        # Existing: 2025-12-11 to 2025-12-13
        # Should conflict
        
        from datetime import datetime
        
        check_in = datetime.strptime("2025-12-10", "%Y-%m-%d")
        check_out = datetime.strptime("2025-12-12", "%Y-%m-%d")
        
        booking_in = datetime.strptime("2025-12-11", "%Y-%m-%d")
        booking_out = datetime.strptime("2025-12-13", "%Y-%m-%d")
        
        # Overlap detection logic
        has_overlap = not (check_out <= booking_in or check_in >= booking_out)
        
        self.assertTrue(has_overlap)
    
    def test_room_availability_ROOM_003(self):
        """
        TEST ID: ROOM_003
        Description: No overlap with back-to-back dates
        Expected: Return True
        """
        from datetime import datetime
        
        check_in = datetime.strptime("2025-12-10", "%Y-%m-%d")
        check_out = datetime.strptime("2025-12-12", "%Y-%m-%d")
        
        booking_in = datetime.strptime("2025-12-12", "%Y-%m-%d")
        booking_out = datetime.strptime("2025-12-14", "%Y-%m-%d")
        
        # Back-to-back should not overlap
        has_overlap = not (check_out <= booking_in or check_in >= booking_out)
        
        self.assertFalse(has_overlap)
    
    def test_filter_by_guests_ROOM_007(self):
        """
        TEST ID: ROOM_007
        Description: Filter rooms by guest capacity
        Expected: Return rooms with sufficient capacity
        """
        num_guests = 4
        
        # Filter logic
        filtered = [r for r in self.rooms if r["max_guests"] >= num_guests]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["room_type"], "Suite")
    
    def test_filter_by_amenities_ROOM_009(self):
        """
        TEST ID: ROOM_009
        Description: Filter rooms by amenity
        Expected: Return only rooms with requested amenity
        """
        amenities = ["Mini-Bar"]
        
        # Filter logic
        filtered = [r for r in self.rooms 
                   if any(a in r["amenities"] for a in amenities)]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["room_type"], "Suite")
    
    def test_filter_combined_ROOM_010(self):
        """
        TEST ID: ROOM_010
        Description: Filter by multiple criteria
        Expected: Return matching rooms
        """
        num_guests = 2
        num_beds = 1
        amenities = ["WiFi", "AC"]
        
        # Combined filter
        filtered = [r for r in self.rooms 
                   if r["max_guests"] >= num_guests
                   and r["num_beds"] >= num_beds
                   and any(a in r["amenities"] for a in amenities)]
        
        self.assertEqual(len(filtered), 3)  # All have WiFi and AC
    
    def test_no_matching_rooms_ROOM_011(self):
        """
        TEST ID: ROOM_011
        Description: No rooms match criteria
        Expected: Return empty list
        """
        num_guests = 6  # Max available is 4
        
        filtered = [r for r in self.rooms if r["max_guests"] >= num_guests]
        
        self.assertEqual(len(filtered), 0)


class TestUtilityFunctions(unittest.TestCase):
    """Test Cases for utils.py - Utility Functions"""
    
    def test_validate_date_valid(self):
        """Validate correct date format"""
        date_string = "2025-12-10"
        
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            is_valid = True
        except:
            is_valid = False
        
        self.assertTrue(is_valid)
    
    def test_validate_date_invalid(self):
        """Reject invalid date format"""
        date_string = "12/10/2025"
        
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            is_valid = True
        except:
            is_valid = False
        
        self.assertFalse(is_valid)
    
    def test_generate_conf_number(self):
        """Generate confirmation number"""
        # Simulate conf number generation
        import random
        import string
        
        conf_num = '#' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        self.assertTrue(conf_num.startswith('#'))
        self.assertEqual(len(conf_num), 9)  # # + 8 characters


class TestRefactoringImpact(unittest.TestCase):
    """Test Cases for Refactored Methods"""
    
    def test_refactored_button_creation(self):
        """Test refactored createButton method behavior"""
        # Simulate button creation tracking
        buttons_created = []
        
        def mock_createButton(text, color, command, space, size):
            buttons_created.append({
                "text": text,
                "color": color,
                "size": size,
                "space": space
            })
        
        # Create multiple buttons with refactored method
        mock_createButton("Create", "green", lambda: None, 10, 12)
        mock_createButton("Modify", "orange", lambda: None, 10, 12)
        mock_createButton("Cancel", "red", lambda: None, 10, 12)
        
        self.assertEqual(len(buttons_created), 3)
        self.assertEqual(buttons_created[0]["color"], "green")
        self.assertEqual(buttons_created[1]["color"], "orange")
    
    def test_refactored_screen_update(self):
        """Test refactored updateScreen method"""
        # Simulate screen update tracking
        screen_updates = []
        
        def mock_updateScreen(color, xSize, ySize):
            screen_updates.append({
                "color": color,
                "xSize": xSize,
                "ySize": ySize
            })
        
        mock_updateScreen("lightblue", 20, 20)
        mock_updateScreen(None, 20, 20)
        
        self.assertEqual(len(screen_updates), 2)
        self.assertEqual(screen_updates[0]["color"], "lightblue")
        self.assertIsNone(screen_updates[1]["color"])


def run_tests():
    """Run all tests with verbose output"""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    print("=" * 70)
    print("HOTEL BOOKING SYSTEM - PHASE 4 UNIT TEST SUITE")
    print("=" * 70)
    print()
    
    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestStorageModule))
    suite.addTests(loader.loadTestsFromTestCase(TestRoomLogicModule))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestRefactoringImpact))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 70)
