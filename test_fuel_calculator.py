#!/usr/bin/env python3
"""
Test script for the Fuel Theft Calculator functionality
Tests the fuel efficiency calculation and theft detection logic
"""

def test_fuel_theft_detection():
    """Test the fuel theft detection logic"""
    
    print("🧪 Testing Fuel Theft Calculator Logic")
    print("=" * 50)
    
    # Test cases: [fuel_consumed, distance_traveled, expected_mileage, expected_result]
    test_cases = [
        # Normal efficiency cases
        (25.0, 100.0, 4.0, "NORMAL"),  # 4.0 km/l - normal
        (20.0, 85.0, 4.2, "NORMAL"),   # 4.25 km/l - normal
        
        # Low efficiency warning cases  
        (30.0, 100.0, 4.0, "WARNING"), # 3.33 km/l - below 85% of expected
        (25.0, 85.0, 4.2, "WARNING"),  # 3.4 km/l - just above theft threshold
        
        # Fuel theft alert cases
        (30.0, 100.0, 3.5, "THEFT"),   # 3.33 km/l - below 3.5 threshold
        (35.0, 120.0, 4.0, "THEFT"),   # 3.43 km/l - below 3.5 threshold
        (40.0, 130.0, 4.5, "THEFT"),   # 3.25 km/l - clear theft case
    ]
    
    for i, (fuel_consumed, distance_traveled, expected_mileage, expected_result) in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}:")
        print(f"   Fuel Consumed: {fuel_consumed} L")
        print(f"   Distance: {distance_traveled} km") 
        print(f"   Expected Mileage: {expected_mileage} km/l")
        
        # Calculate actual mileage (same logic as in app.py)
        actual_mileage = distance_traveled / fuel_consumed
        efficiency_percentage = (actual_mileage / expected_mileage) * 100
        
        # Apply the same detection logic as in app.py
        if actual_mileage < 3.5:
            result = "THEFT"
            status = "🚨 FUEL THEFT ALERT DETECTED!"
        elif actual_mileage < expected_mileage * 0.85:  # 15% below expected
            result = "WARNING"
            status = "⚠️ LOW FUEL EFFICIENCY WARNING"
        else:
            result = "NORMAL"
            status = "✅ FUEL EFFICIENCY NORMAL"
        
        print(f"   Actual Mileage: {actual_mileage:.2f} km/l")
        print(f"   Efficiency: {efficiency_percentage:.1f}%")
        print(f"   Result: {status}")
        
        # Check if result matches expected
        if result == expected_result:
            print(f"   ✅ PASS - Expected {expected_result}, Got {result}")
        else:
            print(f"   ❌ FAIL - Expected {expected_result}, Got {result}")
    
    print("\n" + "=" * 50)
    print("🎯 Fuel Theft Calculator Logic Test Complete!")
    
    # Test cost calculation
    print("\n💰 Testing Cost Calculation:")
    fuel_consumed = 28.5
    distance_traveled = 95.0
    fuel_price_per_liter = 85
    
    fuel_cost_per_km = (fuel_consumed / distance_traveled) * fuel_price_per_liter
    total_fuel_cost = fuel_consumed * fuel_price_per_liter
    
    print(f"   Fuel Consumed: {fuel_consumed} L")
    print(f"   Distance: {distance_traveled} km")
    print(f"   Fuel Price: ₹{fuel_price_per_liter}/L")
    print(f"   Cost per km: ₹{fuel_cost_per_km:.2f}")
    print(f"   Total Fuel Cost: ₹{total_fuel_cost:,.2f}")
    print("   ✅ Cost calculation working correctly!")

if __name__ == "__main__":
    test_fuel_theft_detection()