#!/usr/bin/env python3
"""
Test to verify if the phone number is the issue
"""

import os
from dotenv import load_dotenv

load_dotenv()

def check_phone_number():
    """Check if the phone number looks valid"""
    print("📞 Phone Number Analysis")
    print("=" * 30)
    
    phone = os.getenv("DEMO_PHONE_NUMBER")
    print(f"Current phone number: {phone}")
    
    if not phone:
        print("❌ No phone number set")
        return
    
    # Check format
    if phone.startswith("+1") and len(phone) == 12:
        print("✅ Format looks correct (US number)")
    else:
        print("⚠️ Format might be incorrect")
        print("   Expected: +1234567890 (12 digits with +1)")
    
    # Check if it's a test number
    test_numbers = ["+14156052729", "+1234567890", "+15551234567"]
    if phone in test_numbers:
        print("⚠️ This appears to be a test/demo number")
        print("   These numbers typically don't receive real calls")
        print("   Try using your actual phone number")
    else:
        print("✅ Not a known test number")
    
    print(f"\n💡 To fix:")
    print(f"1. Edit your .env file")
    print(f"2. Change DEMO_PHONE_NUMBER to your real number")
    print(f"3. Use format: +1234567890")
    print(f"4. Example: DEMO_PHONE_NUMBER=+15551234567")

if __name__ == "__main__":
    check_phone_number()
