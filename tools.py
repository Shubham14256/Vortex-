"""
Custom Tools for Route-Rakshak Logistics Super-App
CrewAI Tools for AI-powered logistics operations
"""

import random
import time
from typing import Dict, Any
from crewai.tools import tool


@tool
def drowsiness_detection_tool(image_path: str) -> str:
    """
    Analyzes driver selfie images to detect drowsiness and fatigue levels for safety monitoring
    
    Args:
        image_path: Path to driver selfie image
    Returns:
        Safety status: "Safe" or "Drowsy"
    """
    # Simulate processing time
    time.sleep(0.5)
    
    # Mock detection logic based on keywords for testing
    if "tired" in image_path.lower() or "sleepy" in image_path.lower():
        return "Drowsy - Alert: Driver shows signs of fatigue. Recommend immediate rest break."
    elif "alert" in image_path.lower() or "fresh" in image_path.lower():
        return "Safe - Driver appears alert and focused. Continue journey safely."
    else:
        # Random detection for realistic simulation
        safety_status = random.choice([
            "Safe - Driver appears alert and focused. Continue journey safely.",
            "Safe - Good eye contact and posture detected.",
            "Drowsy - Alert: Driver shows signs of fatigue. Recommend immediate rest break.",
            "Drowsy - Warning: Detected droopy eyelids. Pull over safely."
        ])
        return safety_status


@tool
def engine_diagnosis_tool(audio_path: str) -> str:
    """
    Analyzes engine audio recordings to diagnose mechanical issues and maintenance needs
    
    Args:
        audio_path: Path to engine audio recording
    Returns:
        Diagnosis result with recommendations
    """
    # Simulate processing time
    time.sleep(0.8)
    
    # Mock diagnosis based on keywords for testing
    if "knock" in audio_path.lower() or "rattle" in audio_path.lower():
        return "Engine Issue Detected - Piston knocking sound. Schedule immediate maintenance."
    elif "smooth" in audio_path.lower() or "healthy" in audio_path.lower():
        return "Engine Healthy - All systems operating normally. Next service in 5000 km."
    else:
        # Random diagnosis for realistic simulation
        diagnoses = [
            "Engine Healthy - All systems operating normally. Next service in 5000 km.",
            "Minor Issue - Belt tension needs adjustment. Schedule maintenance within 1000 km.",
            "Engine Issue Detected - Unusual vibration pattern. Inspect engine mounts.",
            "Critical Alert - Irregular combustion detected. Stop vehicle and call mechanic.",
            "Maintenance Due - Oil change required. Engine performance optimal otherwise.",
            "Filter Alert - Air filter replacement needed. Slight performance impact detected."
        ]
        return random.choice(diagnoses)


@tool
def market_search_tool(current_location: str) -> str:
    """
    Searches for available return loads and cargo opportunities to maximize revenue and reduce empty miles
    
    Args:
        current_location: Current location of the vehicle
    Returns:
        JSON string with load details
    """
    # Simulate search processing time
    time.sleep(1.2)
    
    # Dynamic and realistic market data - changes every time!
    import random
    
    # Realistic route combinations from major Indian cities
    route_options = [
        f"{current_location} → Mumbai",
        f"{current_location} → Delhi", 
        f"{current_location} → Bangalore",
        f"{current_location} → Chennai",
        f"{current_location} → Pune",
        f"{current_location} → Hyderabad",
        f"{current_location} → Kolkata",
        f"{current_location} → Ahmedabad",
        f"{current_location} → Nashik",
        f"{current_location} → Coimbatore"
    ]
    
    # Realistic cargo types in Indian logistics
    cargo_types = [
        "Auto Parts", "Textiles", "Steel Coils", "Pharmaceuticals",
        "Electronics", "Agricultural Products", "Chemicals", "Machinery",
        "Consumer Goods", "Raw Materials", "Food Products", "Cement",
        "Plastic Goods", "Paper Products", "Furniture", "Garments"
    ]
    
    # Realistic company names
    companies = [
        "Tata Motors Ltd", "Mahindra Logistics", "Reliance Industries",
        "Bajaj Auto", "TVS Motors", "Hero MotoCorp", "Maruti Suzuki",
        "Godrej Industries", "ITC Limited", "Hindustan Unilever",
        "Asian Paints", "Wipro Limited", "Infosys Technologies",
        "L&T Construction", "Adani Group", "Bharti Enterprises"
    ]
    
    # Generate completely random load opportunity
    selected_route = random.choice(route_options)
    selected_cargo = random.choice(cargo_types)
    selected_company = random.choice(companies)
    
    # Dynamic pricing based on cargo type and distance
    base_prices = {
        "Auto Parts": (25000, 45000),
        "Textiles": (15000, 30000), 
        "Steel Coils": (30000, 55000),
        "Pharmaceuticals": (35000, 60000),
        "Electronics": (40000, 70000),
        "Agricultural Products": (10000, 25000),
        "Chemicals": (20000, 40000),
        "Machinery": (45000, 80000)
    }
    
    price_range = base_prices.get(selected_cargo, (15000, 45000))
    selected_price = random.randint(price_range[0], price_range[1])
    
    # Random weight and distance
    weight = round(random.uniform(2.5, 15.0), 1)
    distance = random.randint(180, 650)
    delivery_time = random.randint(8, 48)
    
    # Priority levels
    priorities = ["Low", "Medium", "High", "Critical", "Urgent"]
    selected_priority = random.choice(priorities)
    
    # Profit margin calculation
    profit_margin = random.randint(12, 38)
    
    # Market conditions (adds realism)
    market_conditions = [
        "High Demand", "Moderate Demand", "Peak Season", "Off Season",
        "Competitive Market", "Premium Route", "Express Delivery"
    ]
    market_condition = random.choice(market_conditions)
    
    # Generate unique search result every time
    search_result = {
        "Status": "Load Found",
        "Search_Time": f"{random.uniform(0.8, 2.5):.1f} seconds",
        "Market_Condition": market_condition,
        "Load_Details": {
            "Route": selected_route,
            "Item": selected_cargo,
            "Weight": f"{weight} tons",
            "Price": selected_price,
            "Distance": f"{distance} km",
            "Delivery_Time": f"{delivery_time} hours",
            "Client": selected_company,
            "Priority": selected_priority
        },
        "Financial_Analysis": {
            "Revenue": f"₹{selected_price:,}",
            "Profit_Margin": f"{profit_margin}%",
            "Rate_per_km": f"₹{selected_price//distance:.0f}/km"
        }
    }
    
    # Return as formatted string for better LLM processing
    return f"""
    🔍 LIVE MARKET SEARCH RESULTS:
    Status: {search_result['Status']} ⚡ {search_result['Search_Time']}
    Market: {search_result['Market_Condition']}
    
    📦 AVAILABLE LOAD OPPORTUNITY:
    Route: {search_result['Load_Details']['Route']}
    Cargo: {search_result['Load_Details']['Item']}
    Weight: {search_result['Load_Details']['Weight']}
    Distance: {search_result['Load_Details']['Distance']}
    Delivery: {search_result['Load_Details']['Delivery_Time']}
    Client: {search_result['Load_Details']['Client']}
    Priority: {search_result['Load_Details']['Priority']}
    
    💰 FINANCIAL BREAKDOWN:
    Total Revenue: {search_result['Financial_Analysis']['Revenue']}
    Profit Margin: {search_result['Financial_Analysis']['Profit_Margin']}
    Rate per KM: {search_result['Financial_Analysis']['Rate_per_km']}
    
    🎯 RECOMMENDATION: {"ACCEPT - Excellent opportunity!" if profit_margin > 25 else "CONSIDER - Good market rate" if profit_margin > 15 else "NEGOTIATE - Below average margin"}
    """


@tool
def expense_validator_tool(amount: float, item: str, category: str = "General") -> str:
    """
    Validates and audits driver expenses, fuel costs, and operational expenditures for compliance
    
    Args:
        amount: Expense amount in rupees
        item: Description of the expense item
        category: Expense category (Fuel, Food, Maintenance, etc.)
    Returns:
        Validation result with approval status
    """
    # Simulate validation processing
    time.sleep(0.3)
    
    # Define expense limits by category
    expense_limits = {
        "Fuel": 10000,
        "Food": 2000,
        "Maintenance": 15000,
        "Toll": 3000,
        "Parking": 500,
        "General": 5000
    }
    
    # Get limit for category
    limit = expense_limits.get(category, 5000)
    
    # Validation logic
    if amount <= limit * 0.5:  # Under 50% of limit
        status = "Auto-Approved"
        risk_level = "Low"
        action_required = "None"
    elif amount <= limit:  # Under limit but higher amount
        status = "Approved"
        risk_level = "Medium"
        action_required = "Manager Notification"
    elif amount <= limit * 1.5:  # Slightly over limit
        status = "Requires Manual Review"
        risk_level = "High"
        action_required = "Finance Team Review"
    else:  # Significantly over limit
        status = "Rejected - Exceeds Policy"
        risk_level = "Critical"
        action_required = "Senior Management Approval Required"
    
    # Generate validation result
    compliance_score = min(100, int((limit / max(amount, 1)) * 100))
    reference_id = f"EXP-{random.randint(100000, 999999)}"
    
    # Add specific recommendations
    if amount > limit:
        recommendation = f"Expense exceeds {category} limit by ₹{amount - limit:,.2f}. Provide additional documentation."
    else:
        recommendation = "Expense within policy limits. Processing approved."
    
    # Return formatted validation result
    return f"""
    💳 EXPENSE VALIDATION REPORT:
    
    📋 EXPENSE DETAILS:
    Amount: ₹{amount:,.2f}
    Item: {item}
    Category: {category}
    Policy Limit: ₹{limit:,}
    
    ✅ VALIDATION RESULT:
    Status: {status}
    Risk Level: {risk_level}
    Action Required: {action_required}
    Compliance Score: {compliance_score}%
    
    📝 RECOMMENDATION:
    {recommendation}
    
    🔍 AUDIT TRAIL:
    Validation Time: {time.strftime("%Y-%m-%d %H:%M:%S")}
    Reference ID: {reference_id}
    """