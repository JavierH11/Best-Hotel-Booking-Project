# 🚀 QUICK START GUIDE

## Setup in 5 Minutes

### 1️⃣ Copy Files to Same Folder
Make sure these 4 files are in the same directory:
```
models.py
controllers.py
main.py
gui_app.py
```

### 2️⃣ Open Command Prompt/Terminal

### 3️⃣ Run the Application
```bash
python gui_app.py
```

### 4️⃣ You're Done! 🎉

---

## 📝 Test User Stories

### Story 1: Create Reservation
- Click "✨ Create New Reservation"
- Enter dates (format: YYYY-MM-DD)
- Select room and amenities
- Fill personal details
- ✅ Get confirmation number

### Story 2: Modify Reservation
- Click "📝 Modify Reservation"
- Enter any confirmation number (e.g., CONF-ABC12345)
- Select new dates
- ✅ See price difference
- ✅ Get new confirmation

### Story 3: Cancel Reservation
- Click "❌ Cancel Reservation"
- Enter confirmation number
- Review booking
- ✅ Confirm cancellation
- ✅ Get cancellation confirmation

### Story 4: Generate Report (Admin)
- Click "📊 Generate Report (Admin)"
- Login: ADMIN001 / admin123
- Select export option
- ✅ Report downloaded as .txt

### Story 5: Unavailable Dates
- Try selecting dates with no availability
- ✅ See error message
- ✅ Option to try different dates

---

## 🔐 Admin Credentials
```
Username: ADMIN001
Password: admin123
```

---

## 🎨 Sample Rooms Available
- Single Room: $100/night
- Double Room: $150/night
- Suite: $250/night

---

## ❓ Common Issues

**Q: "ModuleNotFoundError: No module named 'models'"**
- A: Make sure all 4 .py files are in the same folder

**Q: Date format error**
- A: Use YYYY-MM-DD format (e.g., 2024-12-25)

**Q: Tkinter not found on Linux**
- A: Run `sudo apt-get install python3-tk`

---

## ✨ Features Implemented

✅ Create Reservation (User Story 1)
✅ Modify Reservation (User Story 2)
✅ Cancel Reservation (User Story 3)
✅ Admin Reports (User Story 4)
✅ Error Handling (User Story 5)
✅ Payment Processing
✅ Email Notifications (Simulated)
✅ Unique Confirmation Numbers
✅ Room Filtering by Guests/Beds/Amenities
✅ Price Calculation
✅ Date Validation

---

**Version 1.0 - Ready to Use! 🚀**
