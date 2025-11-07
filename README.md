# Hotel Booking System - Complete GUI Application

## 📋 Overview

This is a complete **Hotel Booking System** with a full Tkinter GUI implementation covering all 5 user stories:

1. ✅ **Hotel guest books room without errors**
2. ✅ **Hotel guest modifies a previous reservation**
3. ✅ **Hotel guest cancels a previous reservation**
4. ✅ **Administrator generates a management report**
5. ✅ **Hotel guest attempts to book unavailable dates**

---

## 📁 Project Structure

```
hotel-booking-system/
├── models.py              # Data models (Room, Reservation, Payment, etc.)
├── controllers.py         # Business logic (ReservationController, PaymentController, etc.)
├── main.py               # Core system (HotelBookingSystem orchestrator)
├── gui_app.py            # Tkinter GUI - ALL USER STORIES IMPLEMENTED
└── README.md             # This file
```

---

## 🚀 Installation & Setup

### Step 1: Install Python (3.8+)
Make sure you have Python installed. Check with:
```bash
python --version
```

### Step 2: Create Virtual Environment
```bash
python -m venv env
```

Activate it:
- **Windows**: `env\Scripts\activate`
- **Mac/Linux**: `source env/bin/activate`

### Step 3: Install Dependencies
Tkinter comes built-in with Python. If you're on Linux and don't have it:
```bash
sudo apt-get install python3-tk
```

### Step 4: Copy All Files
Copy these 4 files to the same folder:
- `models.py`
- `controllers.py`
- `main.py`
- `gui_app.py`

### Step 5: Run the Application
```bash
python gui_app.py
```

---

## 🎯 User Stories Implementation

### **User Story 1: Book Room Without Errors**
✅ **Flow:**
1. Click "✨ Create New Reservation" from homepage
2. Enter check-in and check-out dates
3. Filter rooms by: guests, beds, amenities (at least one)
4. Select a room from available options
5. Enter personal details (name, email, phone, card)
6. Confirm booking → Get confirmation number
7. Email is automatically sent

**Key Features:**
- Real-time room filtering
- Automatic price calculation
- Unique confirmation numbers
- Email notifications (simulated)
- Return to homepage option

---

### **User Story 2: Modify Reservation**
✅ **Flow:**
1. Click "📝 Modify Reservation" from homepage
2. Enter confirmation number
3. System finds the reservation
4. Select new dates and rooms
5. Review old vs new booking (price comparison)
6. Confirm modification
7. Old reservation cancelled, new one created
8. Emails sent for both cancellation and new booking

**Key Features:**
- Old vs new price comparison
- Automatic payment recalculation
- Dual email notifications
- Original confirmation preserved in records

---

### **User Story 3: Cancel Reservation**
✅ **Flow:**
1. Click "❌ Cancel Reservation" from homepage
2. Enter confirmation number
3. View booking details
4. Confirm cancellation
5. Get cancellation confirmation number
6. Email confirmation sent

**Key Features:**
- Detailed booking review before cancellation
- Cancellation confirmation number generation
- Automated email notification
- Immediate status updates

---

### **User Story 4: Generate Management Report**
✅ **Flow:**
1. Click "📊 Generate Report (Admin)" from homepage
2. Enter admin credentials (user: ADMIN001, pwd: admin123)
3. Select report type:
   - Export All Bookings
   - Custom Date Range
4. Report generated as .txt file
5. File automatically downloads

**Test Credentials:**
- Username: `ADMIN001`
- Password: `admin123`

**Key Features:**
- Secure authentication
- Multiple report options
- .txt file export
- Timestamp included
- Complete booking summaries

---

### **User Story 5: Unavailable Dates Error Handling**
✅ **Flow:**
1. If user selects dates with no availability
2. System shows error message
3. User can try different dates or return to homepage

**Key Features:**
- Error validation
- Date availability checking
- User-friendly error messages
- Alternative action options

---

## 🎨 GUI Features

### Homepage
- 4 main action buttons for different use cases
- Clean, organized layout
- Easy navigation

### Navigation
- "Back to Homepage" button on every screen
- Breadcrumb-style flow
- Non-linear navigation support

### Data Entry
- Date pickers with format validation
- Multi-select checkboxes for amenities
- Numeric spinners for guest/bed counts
- Credit card input fields

### Confirmations
- Unique confirmation numbers
- Success/Error messages
- Email simulation display
- Detailed booking summaries

---

## 🔐 Admin Login

**Test Credentials:**
```
Username: ADMIN001
Password: admin123
```

---

## 📊 Sample Data

The system automatically initializes with:

**Rooms:**
- Room R001: Single (1 guest) - $100/night
- Room R002: Double (2 guests) - $150/night
- Room R003: Suite (4 guests) - $250/night

**Amenities:**
- WiFi
- Air Conditioning
- Bathtub
- Kitchen
- Jacuzzi

**Availability:**
- All rooms available for next 60 days

---

## 🔧 Customization

### Add More Rooms
Edit `gui_app.py` in `setup_sample_data()`:
```python
self.system.add_room("R004", "Deluxe", 3, 200.0)
```

### Change Room Prices
Modify the price parameter in `add_room()` call.

### Add Admin Users
Edit `setup_sample_data()`:
```python
self.system.register_user("ADMIN002", "Manager", "manager@hotel.com", "password")
```

### Modify Email Simulation
Edit `send_email_simulation()` method to add real email sending (using `smtplib`).

---

## 📝 Key Classes & Methods

### HotelBookingSystem (main.py)
- `register_user()` - Register new users
- `add_room()` - Add rooms to system
- `create_reservation()` - Create new booking
- `modify_reservation()` - Update existing booking
- `cancel_reservation()` - Cancel booking
- `process_payment()` - Process payment
- `generate_booking_report()` - Create reports

### HotelBookingGUI (gui_app.py)
- `show_homepage()` - Main menu
- `show_create_reservation()` - User Story 1
- `show_modify_reservation()` - User Story 2
- `show_cancel_reservation()` - User Story 3
- `show_admin_login()` - User Story 4
- `show_room_selection()` - Room filtering

---

## 🐛 Troubleshooting

### Tkinter Not Found
```bash
# Windows
python -m pip install tk

# Mac
brew install python-tk

# Linux
sudo apt-get install python3-tk
```

### Import Errors
Make sure all 4 files are in the same directory:
- models.py
- controllers.py
- main.py
- gui_app.py

### Date Format Error
Use format: **YYYY-MM-DD** (e.g., 2024-12-15)

---

## ✨ Features Summary

| Feature | Status |
|---------|--------|
| Create Reservation | ✅ Complete |
| Modify Reservation | ✅ Complete |
| Cancel Reservation | ✅ Complete |
| Generate Reports | ✅ Complete |
| Admin Authentication | ✅ Complete |
| Room Filtering | ✅ Complete |
| Payment Processing | ✅ Complete |
| Email Notifications | ✅ Simulated |
| Confirmation Numbers | ✅ Generated |
| Date Validation | ✅ Implemented |
| Error Handling | ✅ Complete |
| GUI Interface | ✅ Tkinter |

---

## 🚀 Future Enhancements

- Real email sending with SMTP
- Database persistence (SQLite/MySQL)
- Email templates
- Receipt generation
- Guest reviews/ratings
- Cancellation refund policies
- Multi-language support
- Mobile app version
- API endpoints
- Payment gateway integration

---

## 📞 Support

For issues or questions, refer to the inline comments in each Python file.

---

**Version:** 1.0  
**Created:** 2025  
**Language:** Python 3.8+  
**GUI Framework:** Tkinter

🎉 **Ready to use! Just run: `python gui_app.py`**
