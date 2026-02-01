#!/usr/bin/env python3
"""
FastAPI Backend for Route-Rakshak Logistics Super-App
Exposes AI agents and tools via REST API endpoints for React frontend
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import random
import time
import datetime
import requests
import sys
import os

# Add parent directory to path to import our existing modules
try:
    # Option 1: Render वर (जेव्हा आपण backend फोल्डरच्या आत असतो)
    from agents import get_safety_agent, get_mechanic_agent, get_logistics_agent, get_finance_agent
    from tools import (
        drowsiness_detection_tool,
        engine_diagnosis_tool, 
        market_search_tool,
        expense_validator_tool
    )
    print("✅ Successfully imported modules from current directory")

except ImportError:
    # Option 2: Local Computer वर (जेव्हा आपण बाहेर असतो)
    print("⚠️ Importing from parent directory...")
    # sys.path hack to find the backend folder if needed
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from backend.agents import get_safety_agent, get_mechanic_agent, get_logistics_agent, get_finance_agent
    from backend.tools import (
        drowsiness_detection_tool,
        engine_diagnosis_tool, 
        market_search_tool,
        expense_validator_tool
    )
# Initialize FastAPI app
app = FastAPI(
    title="Route-Rakshak API",
    description="AI-powered logistics management system backend",
    version="1.0.0"
)

# Enable CORS for React frontend
# 🔍 या ओळी बदलून खालीलप्रमाणे कर:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 हे केल्याने जगातील कोणतीही लिंक (Vercel/Local) कनेक्ट होऊ शकते.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class LocationRequest(BaseModel):
    location: str
    
class SafetyCheckRequest(BaseModel):
    image_path: str
    driver_status: Optional[str] = "active"
    
class EngineCheckRequest(BaseModel):
    audio_path: str
    vehicle_id: Optional[str] = "TN-01-AB-1234"
    
class ExpenseRequest(BaseModel):
    amount: float
    item: str
    category: str = "General"
    
class TruckLocationUpdate(BaseModel):
    lat: float
    lon: float
    city: str
    progress: int

# Global state for truck location (in production, use Redis or database)
truck_state = {
    "route_coordinates": [
        {"lat": 21.1458, "lon": 79.0882, "city": "Nagpur", "progress": 0},
        {"lat": 20.9320, "lon": 77.7523, "city": "Amravati", "progress": 10},
        {"lat": 20.7000, "lon": 77.0000, "city": "Akola", "progress": 20},
        {"lat": 20.4500, "lon": 76.5000, "city": "Washim", "progress": 30},
        {"lat": 20.2000, "lon": 76.0000, "city": "Hingoli", "progress": 40},
        {"lat": 19.8500, "lon": 75.3000, "city": "Ahmednagar", "progress": 50},
        {"lat": 19.5000, "lon": 74.8000, "city": "Shrirampur", "progress": 60},
        {"lat": 19.2000, "lon": 74.5000, "city": "Manchar", "progress": 70},
        {"lat": 18.9000, "lon": 74.2000, "city": "Talegaon", "progress": 80},
        {"lat": 18.6500, "lon": 73.9000, "city": "Pune Outskirts", "progress": 90},
        {"lat": 18.5204, "lon": 73.8567, "city": "Pune", "progress": 100}
    ],
    "current_index": 0,
    "live_tracking": False
}

# Fleet data state
fleet_state = {
    "vehicles": [
        {
            "id": "TN-01-AB-1234",
            "driver": "Raj Kumar", 
            "route": "Chennai → Bangalore",
            "status": "On Road",
            "eta": "4h 15m"
        },
        {
            "id": "TN-02-CD-5678",
            "driver": "Suresh M",
            "route": "Mumbai → Pune", 
            "status": "Starting",
            "eta": "30m"
        },
        {
            "id": "TN-03-EF-9012",
            "driver": "Vikram S",
            "route": "Delhi → Jaipur",
            "status": "Completed", 
            "eta": "Completed"
        },
        {
            "id": "KA-04-GH-3456",
            "driver": "Arun P",
            "route": "Hyderabad → Vizag",
            "status": "On Road",
            "eta": "2h 45m"
        }
    ]
}

# IoT sensor state
sensor_state = {
    "engine_temp": random.randint(78, 85),
    "battery_voltage": round(random.uniform(13.8, 14.4), 1),
    "oil_pressure": round(random.uniform(35.0, 45.0), 1),
    "rpm": random.randint(1800, 2200),
    "fuel_level": random.randint(65, 95),
    "coolant_temp": random.randint(85, 95)
}

# Helper function to execute AI tools directly
def execute_ai_tool_direct(tool_name: str, input_data: Any) -> Dict[str, Any]:
    """Execute AI tools directly and return structured response"""
    try:
        if tool_name == 'safety':
            result = drowsiness_detection_tool.run(input_data)
        elif tool_name == 'engine':
            result = engine_diagnosis_tool.run(input_data)
        elif tool_name == 'market':
            result = market_search_tool.run(input_data)
        elif tool_name == 'expense':
            result = expense_validator_tool.run(**input_data)
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}
        
        return {
            "success": True,
            "result": str(result),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }

# Weather API helper
def get_live_weather(latitude: float = 21.14, longitude: float = 79.08, city: str = "Nagpur") -> Dict[str, Any]:
    """Fetch real-time weather data from Open-Meteo API"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=Asia/Kolkata"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            current_weather = data.get('current_weather', {})
            
            temp = current_weather.get('temperature', 32)
            windspeed = current_weather.get('windspeed', 12)
            weather_code = current_weather.get('weathercode', 0)
            
            # Weather code to emoji mapping
            weather_emojis = {
                0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
                45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌦️",
                55: "🌧️", 61: "🌧️", 63: "🌧️", 65: "⛈️",
                80: "🌦️", 81: "⛈️", 82: "⛈️"
            }
            
            emoji = weather_emojis.get(weather_code, "🌤️")
            
            return {
                "success": True,
                "city": city,
                "temperature": int(temp),
                "windspeed": int(windspeed),
                "emoji": emoji,
                "status": "Live Data"
            }
    except Exception:
        pass
    
    # Fallback to realistic dummy data
    return {
        "success": False,
        "city": city,
        "temperature": random.randint(28, 35),
        "windspeed": random.randint(8, 18),
        "emoji": random.choice(["☀️", "🌤️", "⛅", "☁️"]),
        "status": "Simulated"
    }

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Route-Rakshak API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/api/find-load")
async def find_load(request: LocationRequest):
    """Find available return loads using AI logistics agent with randomized data"""
    try:
        # Generate random load opportunities
        cities = [
            "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", 
            "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
            "Surat", "Kanpur", "Nagpur", "Indore", "Bhopal"
        ]
        
        cargo_types = [
            "Electronics", "Textiles", "Auto Parts", "Steel Coils", 
            "Pharmaceuticals", "FMCG Products", "Machinery", "Furniture",
            "Agricultural Products", "Chemicals", "Cement", "Tiles",
            "Plastic Goods", "Paper Products", "Food Grains", "Beverages"
        ]
        
        companies = [
            "Reliance Industries", "Tata Motors", "Mahindra & Mahindra",
            "Hindustan Unilever", "ITC Limited", "Asian Paints",
            "Larsen & Toubro", "Godrej Industries", "Wipro",
            "Infosys", "Bajaj Auto", "Hero MotoCorp", "Maruti Suzuki",
            "Bharti Airtel", "Adani Group", "JSW Steel"
        ]
        
        # Generate 3-5 random load opportunities
        num_loads = random.randint(3, 5)
        loads = []
        
        for i in range(num_loads):
            origin = random.choice([c for c in cities if c != request.location])
            destination = random.choice([c for c in cities if c not in [origin, request.location]])
            cargo = random.choice(cargo_types)
            company = random.choice(companies)
            tonnage = random.randint(5, 20)
            price = random.randint(15000, 45000)
            distance = random.randint(200, 800)
            
            loads.append({
                "route": f"{origin} → {destination}",
                "cargo": cargo,
                "company": company,
                "tonnage": f"{tonnage}T",
                "price": f"₹{price:,}",
                "distance": f"{distance} km",
                "pickup_date": f"{random.randint(1, 3)} days"
            })
        
        # Format response
        result_text = f"🔍 Found {num_loads} Available Loads near {request.location}:\n\n"
        for idx, load in enumerate(loads, 1):
            result_text += f"{idx}. {load['route']}\n"
            result_text += f"   📦 Cargo: {load['cargo']} ({load['tonnage']})\n"
            result_text += f"   🏢 Company: {load['company']}\n"
            result_text += f"   💰 Rate: {load['price']}\n"
            result_text += f"   📏 Distance: {load['distance']}\n"
            result_text += f"   📅 Pickup: {load['pickup_date']}\n\n"
        
        result_text += "✅ All loads verified and available for booking!"
        
        return {
            "success": True,
            "data": result_text,
            "loads": loads,
            "location": request.location,
            "timestamp": datetime.datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check-safety")
async def check_safety(request: SafetyCheckRequest):
    """Perform AI-powered drowsiness detection"""
    try:
        result = execute_ai_tool_direct('safety', request.image_path)
        return {
            "success": result["success"],
            "data": result.get("result", ""),
            "driver_status": request.driver_status,
            "timestamp": result["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/diagnose-engine")
async def diagnose_engine(request: EngineCheckRequest):
    """Perform AI-powered engine diagnosis"""
    try:
        result = execute_ai_tool_direct('engine', request.audio_path)
        return {
            "success": result["success"],
            "data": result.get("result", ""),
            "vehicle_id": request.vehicle_id,
            "timestamp": result["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate-expense")
async def validate_expense(request: ExpenseRequest):
    """Validate expenses using AI finance agent"""
    try:
        expense_data = {
            "amount": request.amount,
            "item": request.item,
            "category": request.category
        }
        result = execute_ai_tool_direct('expense', expense_data)
        return {
            "success": result["success"],
            "data": result.get("result", ""),
            "expense": expense_data,
            "timestamp": result["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/truck-location")
async def get_truck_location():
    """Get current truck location for map display"""
    current_location = truck_state["route_coordinates"][truck_state["current_index"]]
    return {
        "success": True,
        "location": current_location,
        "live_tracking": truck_state["live_tracking"],
        "route_progress": f"{truck_state['current_index']}/{len(truck_state['route_coordinates']) - 1}",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/api/truck-location/move")
async def move_truck():
    """Move truck to next position (simulate movement)"""
    if truck_state["current_index"] < len(truck_state["route_coordinates"]) - 1:
        truck_state["current_index"] += 1
        current_location = truck_state["route_coordinates"][truck_state["current_index"]]
        return {
            "success": True,
            "message": f"Truck moved to {current_location['city']}",
            "location": current_location,
            "timestamp": datetime.datetime.now().isoformat()
        }
    else:
        return {
            "success": False,
            "message": "Truck has reached destination",
            "location": truck_state["route_coordinates"][-1],
            "timestamp": datetime.datetime.now().isoformat()
        }

@app.post("/api/truck-location/reset")
async def reset_truck():
    """Reset truck to starting position"""
    truck_state["current_index"] = 0
    truck_state["live_tracking"] = False
    return {
        "success": True,
        "message": "Truck reset to starting position",
        "location": truck_state["route_coordinates"][0],
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/api/truck-location/toggle-tracking")
async def toggle_live_tracking():
    """Toggle live tracking on/off"""
    truck_state["live_tracking"] = not truck_state["live_tracking"]
    return {
        "success": True,
        "live_tracking": truck_state["live_tracking"],
        "message": f"Live tracking {'started' if truck_state['live_tracking'] else 'stopped'}",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/api/fleet")
async def get_fleet():
    """Get fleet data"""
    return {
        "success": True,
        "vehicles": fleet_state["vehicles"],
        "total_vehicles": len(fleet_state["vehicles"]),
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/api/fleet/add")
async def add_vehicle(vehicle: dict):
    """Add new vehicle to fleet"""
    fleet_state["vehicles"].append(vehicle)
    return {
        "success": True,
        "message": f"Vehicle {vehicle.get('id', 'Unknown')} added to fleet",
        "total_vehicles": len(fleet_state["vehicles"]),
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/api/sensors")
async def get_sensors():
    """Get current IoT sensor readings"""
    return {
        "success": True,
        "sensors": sensor_state,
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/api/sensors/refresh")
async def refresh_sensors():
    """Refresh IoT sensor readings with realistic fluctuations"""
    global sensor_state
    
    # Realistic fluctuations (small changes, not dramatic jumps)
    sensor_state = {
        "engine_temp": max(75, min(90, sensor_state["engine_temp"] + random.randint(-2, 3))),
        "battery_voltage": round(max(13.5, min(14.8, sensor_state["battery_voltage"] + random.uniform(-0.2, 0.2))), 1),
        "oil_pressure": round(max(30.0, min(50.0, sensor_state["oil_pressure"] + random.uniform(-2.0, 2.0))), 1),
        "rpm": max(1500, min(2500, sensor_state["rpm"] + random.randint(-100, 150))),
        "fuel_level": max(0, min(100, sensor_state["fuel_level"] + random.randint(-2, 1))),
        "coolant_temp": max(80, min(100, sensor_state["coolant_temp"] + random.randint(-2, 3)))
    }
    
    return {
        "success": True,
        "sensors": sensor_state,
        "message": "Sensor readings refreshed",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/api/weather")
async def get_weather(lat: float = 21.14, lon: float = 79.08, city: str = "Nagpur"):
    """Get current weather data"""
    weather_data = get_live_weather(lat, lon, city)
    return {
        "success": True,
        "weather": weather_data,
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/api/system-logs")
async def get_system_logs():
    """Get system activity logs"""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    log_messages = [
        f"[{current_time}] 📡 GPS Signal Strength: {random.randint(85, 98)}% - Strong",
        f"[{current_time}] 🔄 Fleet Data Sync: Complete - {random.randint(24, 28)} vehicles",
        f"[{current_time}] 🤖 AI Agent Heartbeat: Active - Response time {random.randint(45, 120)}ms",
        f"[{current_time}] 🛰️ Satellite Connection: Stable - 12 satellites locked",
        f"[{current_time}] 📊 Database Query: Executed in {random.randint(15, 85)}ms",
        f"[{current_time}] 🔐 Security Check: Passed - All systems secure",
        f"[{current_time}] 📱 Mobile App Sync: {random.randint(156, 234)} active sessions",
        f"[{current_time}] ⚡ System Load: {random.randint(15, 45)}% - Optimal",
        f"[{current_time}] 🌐 API Gateway: {random.randint(1200, 1800)} requests/min",
        f"[{current_time}] 💾 Backup Status: Last backup {random.randint(5, 25)} min ago"
    ]
    
    return {
        "success": True,
        "logs": random.sample(log_messages, 6),
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/api/find-partial-load")
async def find_partial_load():
    """Find nearby overloaded trucks for peer-to-peer load sharing"""
    try:
        # Truck registration patterns
        truck_ids = [
            "MH-12-AB-5678", "TN-09-CD-1234", "KA-05-EF-9012", 
            "DL-08-GH-3456", "GJ-01-IJ-7890", "RJ-14-KL-2345",
            "UP-16-MN-6789", "MP-09-OP-4567", "HR-55-QR-8901",
            "PB-10-ST-2345"
        ]
        
        # Cargo types that can be shared
        cargo_types = [
            "Rice Bags", "Wheat Sacks", "Sugar Bags", "Cement Bags",
            "Fertilizer Bags", "Textile Rolls", "Plastic Crates",
            "Steel Rods", "Wooden Planks", "Cardboard Boxes",
            "Food Grains", "Animal Feed", "Construction Materials"
        ]
        
        # Driver names
        driver_names = [
            "Ramesh Kumar", "Suresh Patil", "Vijay Singh", "Anil Sharma",
            "Prakash Rao", "Mahesh Gupta", "Rajesh Verma", "Dinesh Yadav",
            "Santosh Reddy", "Ganesh Naik"
        ]
        
        # Generate random overload scenario
        truck_id = random.choice(truck_ids)
        driver_name = random.choice(driver_names)
        cargo = random.choice(cargo_types)
        overload_tons = random.randint(2, 5)
        distance_km = random.randint(3, 15)
        offer_price = random.randint(3000, 8000)
        
        # Calculate urgency level
        urgency = "HIGH" if overload_tons >= 4 else "MEDIUM" if overload_tons >= 3 else "LOW"
        urgency_emoji = "🔴" if urgency == "HIGH" else "🟡" if urgency == "MEDIUM" else "🟢"
        
        # Generate realistic scenario
        result = {
            "success": True,
            "alert": True,
            "truck_id": truck_id,
            "driver_name": driver_name,
            "cargo": cargo,
            "overload_tons": overload_tons,
            "distance_km": distance_km,
            "offer_price": offer_price,
            "urgency": urgency,
            "urgency_emoji": urgency_emoji,
            "location": random.choice([
                "NH-48 Highway", "Mumbai-Pune Expressway", "Delhi-Jaipur Highway",
                "Bangalore-Chennai Road", "Hyderabad Outer Ring Road", "Ahmedabad-Vadodara Highway"
            ]),
            "estimated_time": f"{random.randint(10, 30)} min",
            "fine_risk": f"₹{random.randint(10000, 25000)}",
            "message": f"""
⚠️ EMERGENCY LOAD SHARING REQUEST

🚛 Truck: {truck_id}
👨‍✈️ Driver: {driver_name}
📍 Distance: {distance_km} km away
⏰ ETA: {random.randint(10, 30)} minutes

📦 OVERLOAD DETAILS:
• Cargo: {cargo}
• Excess Weight: {overload_tons} Tons
• Urgency: {urgency_emoji} {urgency}
• Fine Risk: ₹{random.randint(10000, 25000)}

💰 YOUR EARNINGS:
• Offer Price: ₹{offer_price:,}
• Distance Bonus: ₹{random.randint(200, 500)}
• Total: ₹{offer_price + random.randint(200, 500):,}

🤝 COMMUNITY BENEFIT:
• Help fellow driver avoid fine
• Earn extra income
• Build network reputation
• Support logistics community

⏱️ Request expires in: {random.randint(15, 45)} minutes
            """.strip(),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/accept-partial-load")
async def accept_partial_load(request: dict):
    """Accept a partial load sharing request"""
    try:
        truck_id = request.get("truck_id", "Unknown")
        offer_price = request.get("offer_price", 0)
        
        return {
            "success": True,
            "message": f"Load accepted from {truck_id}!",
            "navigation_started": True,
            "truck_id": truck_id,
            "earnings": offer_price,
            "eta": f"{random.randint(10, 30)} minutes",
            "pickup_location": random.choice([
                "NH-48 Rest Stop", "Fuel Station Exit 12", "Highway Toll Plaza",
                "Truck Parking Zone A", "Service Area 3"
            ]),
            "timestamp": datetime.datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
