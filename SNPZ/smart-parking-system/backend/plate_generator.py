"""
Indian Number Plate Generator
Generates realistic Indian vehicle registration plates.
Format: [STATE CODE] [DISTRICT] [SERIES] [NUMBER]
"""

import random
import string

# Common Indian state codes with their district ranges
STATE_CODES = {
    "DL": (1, 13),    # Delhi
    "MH": (1, 49),    # Maharashtra
    "UP": (14, 85),   # Uttar Pradesh
    "KA": (1, 65),    # Karnataka
    "TN": (1, 99),    # Tamil Nadu
    "RJ": (1, 53),    # Rajasthan
    "HR": (1, 76),    # Haryana
    "GJ": (1, 39),    # Gujarat
    "AP": (1, 39),    # Andhra Pradesh
    "WB": (1, 78),    # West Bengal
    "MP": (1, 68),    # Madhya Pradesh
    "PB": (1, 75),    # Punjab
    "CH": (1, 4),     # Chandigarh
    "JH": (1, 20),    # Jharkhand
    "BR": (1, 38),    # Bihar
}


def generate_plate():
    """
    Generate a random Indian-style number plate.
    Format: XX 00 XX 0000
    Example: DL 3C AB 1234
    """
    # Pick a random state
    state = random.choice(list(STATE_CODES.keys()))
    
    # District number (1-2 digits)
    district_min, district_max = STATE_CODES[state]
    district = random.randint(district_min, district_max)
    
    # Series letters (1-2 uppercase letters)
    series = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    # 4-digit number (1000-9999 to ensure 4 digits)
    number = random.randint(1000, 9999)
    
    # Format: STATE DISTRICT SERIES NUMBER
    # District is zero-padded to 2 digits
    plate = f"{state} {district:02d} {series} {number}"
    
    return plate


if __name__ == "__main__":
    # Test: generate 10 sample plates
    for _ in range(10):
        print(generate_plate())
