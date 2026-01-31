#!/usr/bin/env python3
"""
Test script for Partial Load Sharing endpoints
Run this after starting the backend server
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_find_partial_load():
    """Test the find partial load endpoint"""
    print("\n" + "="*60)
    print("🔍 Testing: POST /api/find-partial-load")
    print("="*60)
    
    try:
        response = requests.post(f"{BASE_URL}/api/find-partial-load")
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📦 Response Data:")
            print(json.dumps(data, indent=2))
            
            # Verify required fields
            required_fields = [
                'success', 'alert', 'truck_id', 'driver_name', 
                'cargo', 'overload_tons', 'distance_km', 'offer_price',
                'urgency', 'urgency_emoji', 'location', 'estimated_time', 'fine_risk'
            ]
            
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"\n⚠️ Missing fields: {missing_fields}")
            else:
                print(f"\n✅ All required fields present!")
                print(f"\n🚛 Truck: {data['truck_id']}")
                print(f"👨‍✈️ Driver: {data['driver_name']}")
                print(f"📦 Cargo: {data['cargo']} ({data['overload_tons']} tons)")
                print(f"💰 Offer: ₹{data['offer_price']:,}")
                print(f"📍 Distance: {data['distance_km']} km")
                print(f"🚨 Urgency: {data['urgency_emoji']} {data['urgency']}")
            
            return data
        else:
            print(f"\n❌ Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        return None

def test_accept_partial_load(truck_id="MH-12-AB-5678", offer_price=5000):
    """Test the accept partial load endpoint"""
    print("\n" + "="*60)
    print("✅ Testing: POST /api/accept-partial-load")
    print("="*60)
    
    try:
        payload = {
            "truck_id": truck_id,
            "offer_price": offer_price
        }
        
        print(f"\n📤 Request Payload:")
        print(json.dumps(payload, indent=2))
        
        response = requests.post(
            f"{BASE_URL}/api/accept-partial-load",
            json=payload
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📦 Response Data:")
            print(json.dumps(data, indent=2))
            
            # Verify required fields
            required_fields = ['success', 'message', 'navigation_started', 'truck_id', 'earnings', 'eta']
            
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"\n⚠️ Missing fields: {missing_fields}")
            else:
                print(f"\n✅ All required fields present!")
                print(f"\n🎉 {data['message']}")
                print(f"💰 Earnings: ₹{data['earnings']:,}")
                print(f"⏰ ETA: {data['eta']}")
                print(f"🧭 Navigation: {'Started' if data['navigation_started'] else 'Not Started'}")
            
            return data
        else:
            print(f"\n❌ Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        return None

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 PARTIAL LOAD SHARING ENDPOINT TESTS")
    print("="*60)
    print("\n⚠️ Make sure the backend server is running on port 8000!")
    print("   Run: cd backend && python start.py")
    
    input("\nPress Enter to start tests...")
    
    # Test 1: Find partial load
    partial_load_data = test_find_partial_load()
    
    # Test 2: Accept partial load
    if partial_load_data and partial_load_data.get('alert'):
        print("\n" + "-"*60)
        input("\nPress Enter to test accepting this load...")
        test_accept_partial_load(
            truck_id=partial_load_data['truck_id'],
            offer_price=partial_load_data['offer_price']
        )
    else:
        print("\n" + "-"*60)
        print("\n⚠️ No partial load found, testing with dummy data...")
        test_accept_partial_load()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print("\n💡 Next Steps:")
    print("   1. Start the frontend: cd frontend && npm run dev")
    print("   2. Open http://localhost:3001")
    print("   3. Go to Driver Dashboard")
    print("   4. Click 'Scan for Overloaded Trucks'")
    print("   5. Accept or Ignore the load request")
    print("\n")

if __name__ == "__main__":
    main()
