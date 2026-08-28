"""
In-Memory Database Store
Stores all active vehicles, SMS logs, challans, and stats.
This is the single source of truth for the application.
"""

import threading
from datetime import datetime

# Thread lock for safe concurrent access
lock = threading.Lock()

# ── Active vehicles dict: plate -> vehicle data ──
vehicles = {}

# ── SMS log list ──
sms_log = []

# ── Challan records list ──
challans = []

# ── Counters ──
stats = {
    "total_detected": 0,
    "challans_issued": 0,
    "sms_sent": 0,
    "session_date": datetime.now().strftime("%Y-%m-%d"),
}

# ── Challan serial counter ──
challan_counter = 0


def reset_daily_stats():
    """Reset stats if a new day has started."""
    today = datetime.now().strftime("%Y-%m-%d")
    if stats["session_date"] != today:
        stats["total_detected"] = 0
        stats["challans_issued"] = 0
        stats["sms_sent"] = 0
        stats["session_date"] = today


def get_next_challan_id():
    """Generate the next unique challan ID in format CH-YYYYMMDD-XXXX."""
    global challan_counter
    challan_counter += 1
    date_str = datetime.now().strftime("%Y%m%d")
    return f"CH-{date_str}-{challan_counter:04d}"


def add_vehicle(plate, location, gps):
    """Add a new vehicle to active tracking."""
    with lock:
        reset_daily_stats()
        entry_time = datetime.now()
        vehicles[plate] = {
            "plate": plate,
            "entry_time": entry_time.isoformat(),
            "entry_time_dt": entry_time,
            "status": "Monitoring",
            "sms_sent": False,
            "challan_id": None,
            "location": location,
            "gps": gps,
        }
        stats["total_detected"] += 1
        return vehicles[plate]


def remove_vehicle(plate):
    """Remove a vehicle from active tracking (vehicle left the zone)."""
    with lock:
        if plate in vehicles:
            vehicle = vehicles.pop(plate)
            return vehicle
        return None


def get_all_vehicles():
    """Return all active vehicles with computed elapsed time."""
    with lock:
        result = []
        now = datetime.now()
        for plate, v in vehicles.items():
            elapsed_seconds = (now - v["entry_time_dt"]).total_seconds()
            mins = int(elapsed_seconds // 60)
            secs = int(elapsed_seconds % 60)
            result.append({
                "plate": v["plate"],
                "entry_time": v["entry_time"],
                "elapsed_seconds": elapsed_seconds,
                "elapsed_display": f"{mins}m {secs}s",
                "status": v["status"],
                "sms_sent": v["sms_sent"],
                "challan_id": v["challan_id"],
                "location": v["location"],
                "gps": v["gps"],
            })
        return result


def add_sms(plate, message):
    """Log a simulated SMS message."""
    with lock:
        sms_log.append({
            "timestamp": datetime.now().isoformat(),
            "plate": plate,
            "message": message,
        })
        stats["sms_sent"] += 1


def add_challan(challan):
    """Add a challan record."""
    with lock:
        challans.append(challan)
        stats["challans_issued"] += 1


def get_sms_log():
    """Return all SMS log entries."""
    with lock:
        return list(sms_log)


def get_challans():
    """Return all challan records."""
    with lock:
        return list(challans)


def get_stats():
    """Return dashboard statistics."""
    with lock:
        reset_daily_stats()
        return {
            "total_detected": stats["total_detected"],
            "currently_in_zone": len(vehicles),
            "challans_issued": stats["challans_issued"],
            "sms_sent": stats["sms_sent"],
        }
