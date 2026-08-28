"""
Enforcement Engine — Background Thread
Continuously checks all active vehicles and applies the violation logic:
  - >= 5 min → ILLEGAL PARKING → SMS warning → status "SMS Sent"
  - >= 7 min → Challan generation → status "Challan Issued"
"""

import threading
import time
import random
from datetime import datetime

import database as db

# Simulated locations around Delhi
LOCATIONS = [
    "Near AIIMS Gate 1, Ansari Nagar, New Delhi",
    "Connaught Place, Block A, New Delhi",
    "Karol Bagh Metro Station, New Delhi",
    "India Gate, Rajpath, New Delhi",
    "Lajpat Nagar Market, New Delhi",
    "Sarojini Nagar Market, New Delhi",
    "Chandni Chowk, Old Delhi",
    "Nehru Place IT Hub, New Delhi",
    "Hauz Khas Village, New Delhi",
    "Greater Kailash Part 1, New Delhi",
]

BASE_LAT = 28.6139
BASE_LNG = 77.2090


def get_random_location():
    """Return a random Delhi location name."""
    return random.choice(LOCATIONS)


def get_random_gps():
    """Return GPS coordinates with slight random offset from central Delhi."""
    lat = BASE_LAT + random.uniform(-0.08, 0.08)
    lng = BASE_LNG + random.uniform(-0.08, 0.08)
    return {"lat": round(lat, 4), "lng": round(lng, 4)}


def _build_sms_message(plate, location, entry_time):
    """Build the simulated SMS warning message."""
    time_str = entry_time if isinstance(entry_time, str) else entry_time.strftime("%I:%M %p")
    return (
        f"[WARNING] Dear Vehicle Owner of {plate}, your vehicle has been "
        f"parked in a No-Parking Zone at {location} since {time_str}. "
        f"Please move your vehicle immediately or a challan of ₹500 will "
        f"be issued. - Traffic Police"
    )


def _generate_challan(vehicle):
    """Generate a full challan record for the vehicle."""
    challan_id = db.get_next_challan_id()
    now = datetime.now()
    return {
        "challan_id": challan_id,
        "plate": vehicle["plate"],
        "violation_time": now.isoformat(),
        "violation_time_display": now.strftime("%d %b %Y, %I:%M %p"),
        "location": vehicle["location"],
        "gps": vehicle["gps"],
        "fine_amount": 500,
        "status": "Issued",
    }


def enforcement_loop(check_interval=10):
    """
    Main enforcement loop. Runs forever in a daemon thread.
    Checks every `check_interval` seconds.
    """
    while True:
        try:
            now = datetime.now()
            with db.lock:
                for plate, vehicle in list(db.vehicles.items()):
                    elapsed = (now - vehicle["entry_time_dt"]).total_seconds()
                    elapsed_minutes = elapsed / 60.0

                    # ── Stage 1: >= 5 minutes, still Monitoring → ILLEGAL PARKING → SMS ──
                    if elapsed_minutes >= 5 and vehicle["status"] == "Monitoring":
                        vehicle["status"] = "ILLEGAL PARKING"
                        # Immediately send SMS and update status
                        sms_message = _build_sms_message(
                            plate, vehicle["location"], vehicle["entry_time"]
                        )
                        vehicle["status"] = "SMS Sent"
                        vehicle["sms_sent"] = True

                    # ── Stage 2: >= 7 minutes, SMS already sent → Challan ──
                    elif elapsed_minutes >= 7 and vehicle["status"] == "SMS Sent":
                        challan = _generate_challan(vehicle)
                        vehicle["status"] = "Challan Issued"
                        vehicle["challan_id"] = challan["challan_id"]

                # ── Now do the DB writes outside the inner loop but inside lock ──
                # Re-iterate to commit SMS and challans (already mutated above)
                # We need a second pass to add sms/challan records to avoid
                # modifying db.sms_log/challans while holding the lock differently.

            # Second pass — commit SMS and challan records (lock released and re-acquired)
            with db.lock:
                for plate, vehicle in list(db.vehicles.items()):
                    elapsed = (now - vehicle["entry_time_dt"]).total_seconds()
                    elapsed_minutes = elapsed / 60.0

                    # Check if SMS needs to be logged
                    if vehicle["sms_sent"] and vehicle["status"] == "SMS Sent":
                        # Only log if not already logged
                        already_logged = any(
                            s["plate"] == plate for s in db.sms_log
                        )
                        if not already_logged:
                            sms_message = _build_sms_message(
                                plate, vehicle["location"], vehicle["entry_time"]
                            )
                            db.sms_log.append({
                                "timestamp": datetime.now().isoformat(),
                                "plate": plate,
                                "message": sms_message,
                            })
                            db.stats["sms_sent"] += 1

                    # Check if challan needs to be logged
                    if vehicle["challan_id"] and vehicle["status"] == "Challan Issued":
                        already_logged = any(
                            c["challan_id"] == vehicle["challan_id"]
                            for c in db.challans
                        )
                        if not already_logged:
                            challan = _generate_challan(vehicle)
                            challan["challan_id"] = vehicle["challan_id"]
                            db.challans.append(challan)
                            db.stats["challans_issued"] += 1

        except Exception as e:
            print(f"[Enforcement Error] {e}")

        time.sleep(check_interval)


def start_enforcement_thread(check_interval=10):
    """Start the enforcement engine as a background daemon thread."""
    thread = threading.Thread(
        target=enforcement_loop,
        args=(check_interval,),
        daemon=True,
        name="EnforcementThread",
    )
    thread.start()
    print(f"[Enforcement] Background thread started (checking every {check_interval}s)")
    return thread
