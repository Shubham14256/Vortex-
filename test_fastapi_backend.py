#!/usr/bin/env python3
"""
Test script for FastAPI backend
Verifies all API endpoints are working correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the root health check endpoint"""
    print("🧪 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health Check: {data['message']}")
            print(f"   📊 Status: {data['status']}")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   ⚠️  Make sure FastAPI server is running on port 8000")
        return False

def test_truck_location():
    """Test truck location endpoint"""
    print("\n🧪 Testing Truck Location API...")
    try:
        response = requests.get(f"{BASE_URL}/api/truck-location")
        if response.status_code == 200:
            data = response.json()
            location = data['location']
            print(f"   ✅ Current Location: {location['city']}")
            print(f"   📍 Coordinates: ({location['lat']}, {location['lon']})")
            print(f"   📊 Progress: {location['progress']}%")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_find_load():
    """Test find load endpoint"""
    print("\n🧪 Testing Find Load API...")
    try:
        payload = {"location": "Bangalore"}
        response = requests.post(f"{BASE_URL}/api/find-load", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Load Search: Success")
            print(f"   📦 Location: {data['location']}")
            print(f"   🎯 Result Preview: {data['data'][:100]}...")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_sensors():
    """Test IoT sensors endpoint"""
    print("\n🧪 Testing IoT Sensors API...")
    try:
        response = requests.get(f"{BASE_URL}/api/sensors")
        if response.status_code == 200:
            data = response.json()
            sensors = data['sensors']
            print(f"   ✅ Sensor Data Retrieved")
            print(f"   🌡️  Engine Temp: {sensors['engine_temp']}°C")
            print(f"   ⚡ Battery: {sensors['battery_voltage']}V")
            print(f"   🛢️  Oil Pressure: {sensors['oil_pressure']} PSI")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_weather():
    """Test weather API endpoint"""
    print("\n🧪 Testing Weather API...")
    try:
        response = requests.get(f"{BASE_URL}/api/weather?lat=21.14&lon=79.08&city=Nagpur")
        if response.status_code == 200:
            data = response.json()
            weather = data['weather']
            print(f"   ✅ Weather Data Retrieved")
            print(f"   🌤️  {weather['city']}: {weather['temperature']}°C")
            print(f"   💨 Wind: {weather['windspeed']} km/h")
            print(f"   📡 Status: {weather['status']}")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_fleet():
    """Test fleet management endpoint"""
    print("\n🧪 Testing Fleet API...")
    try:
        response = requests.get(f"{BASE_URL}/api/fleet")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Fleet Data Retrieved")
            print(f"   🚛 Total Vehicles: {data['total_vehicles']}")
            print(f"   📋 First Vehicle: {data['vehicles'][0]['id']}")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_system_logs():
    """Test system logs endpoint"""
    print("\n🧪 Testing System Logs API...")
    try:
        response = requests.get(f"{BASE_URL}/api/system-logs")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ System Logs Retrieved")
            print(f"   📟 Log Entries: {len(data['logs'])}")
            print(f"   📝 Sample: {data['logs'][0][:60]}...")
            return True
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🚛 Route-Rakshak FastAPI Backend Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_check()))
    results.append(("Truck Location", test_truck_location()))
    results.append(("Find Load", test_find_load()))
    results.append(("IoT Sensors", test_sensors()))
    results.append(("Weather API", test_weather()))
    results.append(("Fleet Management", test_fleet()))
    results.append(("System Logs", test_system_logs()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n   🎉 All tests passed! Backend is ready for React frontend.")
        print("\n   📚 API Documentation: http://localhost:8000/docs")
        print("   🌐 Backend URL: http://localhost:8000")
    else:
        print("\n   ⚠️  Some tests failed. Please check the backend server.")
        print("   💡 Start the backend with: cd backend && uvicorn main:app --reload")

if __name__ == "__main__":
    main()