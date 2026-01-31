import streamlit as st
import pandas as pd
import time
import os
import folium
from streamlit_folium import st_folium

# CrewAI imports for AI functionality
from crewai import Agent, Task, Crew
from agents import get_safety_agent, get_mechanic_agent, get_logistics_agent, get_finance_agent
from dotenv import load_dotenv
import requests
import random
import datetime

# Load environment variables
load_dotenv()

# Initialize Session State for Data Persistence
def initialize_session_state():
    """Initialize session state with default data if not exists"""
    
    # Fleet data initialization
    if 'fleet_data' not in st.session_state:
        st.session_state['fleet_data'] = [
            {
                'Vehicle ID': 'TN-01-AB-1234',
                'Driver': 'Raj Kumar',
                'Route': 'Chennai → Bangalore',
                'Status': '🛣️ On Road',
                'ETA': '4h 15m'
            },
            {
                'Vehicle ID': 'TN-02-CD-5678',
                'Driver': 'Suresh M',
                'Route': 'Mumbai → Pune',
                'Status': '🚀 Starting',
                'ETA': '30m'
            },
            {
                'Vehicle ID': 'TN-03-EF-9012',
                'Driver': 'Vikram S',
                'Route': 'Delhi → Jaipur',
                'Status': '🏁 Completed',
                'ETA': 'Completed'
            },
            {
                'Vehicle ID': 'KA-04-GH-3456',
                'Driver': 'Arun P',
                'Route': 'Hyderabad → Vizag',
                'Status': '🛣️ On Road',
                'ETA': '2h 45m'
            }
        ]
    
    # Truck location for real-time GPS simulation with predefined route
    if 'truck_location' not in st.session_state:
        # Define 10 coordinates along Nagpur-Pune highway for smooth animation
        st.session_state['route_coordinates'] = [
            {'lat': 21.1458, 'lon': 79.0882, 'city': 'Nagpur', 'progress': 0},      # Start
            {'lat': 20.9320, 'lon': 77.7523, 'city': 'Amravati', 'progress': 10},   # 10%
            {'lat': 20.7000, 'lon': 77.0000, 'city': 'Akola', 'progress': 20},      # 20%
            {'lat': 20.4500, 'lon': 76.5000, 'city': 'Washim', 'progress': 30},     # 30%
            {'lat': 20.2000, 'lon': 76.0000, 'city': 'Hingoli', 'progress': 40},    # 40%
            {'lat': 19.8500, 'lon': 75.3000, 'city': 'Ahmednagar', 'progress': 50}, # 50%
            {'lat': 19.5000, 'lon': 74.8000, 'city': 'Shrirampur', 'progress': 60}, # 60%
            {'lat': 19.2000, 'lon': 74.5000, 'city': 'Manchar', 'progress': 70},    # 70%
            {'lat': 18.9000, 'lon': 74.2000, 'city': 'Talegaon', 'progress': 80},   # 80%
            {'lat': 18.6500, 'lon': 73.9000, 'city': 'Pune Outskirts', 'progress': 90}, # 90%
            {'lat': 18.5204, 'lon': 73.8567, 'city': 'Pune', 'progress': 100}       # End
        ]
        
        st.session_state['truck_location'] = st.session_state['route_coordinates'][0].copy()
        st.session_state['truck_index'] = 0
        st.session_state['live_tracking_active'] = False
    
    # Financial data for charts
    if 'financial_data' not in st.session_state:
        st.session_state['financial_data'] = {
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Income': [45000, 52000, 48000, 61000, 55000, 67000, 45230],
            'Expense': [32000, 38000, 35000, 42000, 39000, 48000, 33000],
            'Profit': [13000, 14000, 13000, 19000, 16000, 19000, 12230]
        }
    
    # Fleet metrics
    if 'fleet_metrics' not in st.session_state:
        st.session_state['fleet_metrics'] = {
            'total_vehicles': len(st.session_state['fleet_data']),
            'active_trips': len([v for v in st.session_state['fleet_data'] if '🛣️' in v['Status']]),
            'available': len([v for v in st.session_state['fleet_data'] if '🚀' in v['Status']]),
            'completed': len([v for v in st.session_state['fleet_data'] if '🏁' in v['Status']]),
            'in_maintenance': len([v for v in st.session_state['fleet_data'] if '🔧' in v['Status']])
        }

# Initialize session state
initialize_session_state()

# Weather API function
def get_live_weather(latitude=21.14, longitude=79.08, city="Nagpur"):
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
    except Exception as e:
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

# IoT Sensor simulation
def get_engine_sensors():
    """Simulate fluctuating engine parameters like real IoT sensors"""
    if 'engine_sensors' not in st.session_state:
        st.session_state['engine_sensors'] = {
            'engine_temp': random.randint(78, 85),
            'battery_voltage': round(random.uniform(13.8, 14.4), 1),
            'oil_pressure': round(random.uniform(35.0, 45.0), 1),
            'rpm': random.randint(1800, 2200),
            'fuel_level': random.randint(65, 95),
            'coolant_temp': random.randint(85, 95)
        }
    
    return st.session_state['engine_sensors']

def refresh_engine_sensors():
    """Refresh engine sensor readings with realistic fluctuations"""
    current = st.session_state.get('engine_sensors', {})
    
    # Realistic fluctuations (small changes, not dramatic jumps)
    st.session_state['engine_sensors'] = {
        'engine_temp': max(75, min(90, current.get('engine_temp', 80) + random.randint(-2, 3))),
        'battery_voltage': round(max(13.5, min(14.8, current.get('battery_voltage', 14.0) + random.uniform(-0.2, 0.2))), 1),
        'oil_pressure': round(max(30.0, min(50.0, current.get('oil_pressure', 40.0) + random.uniform(-2.0, 2.0))), 1),
        'rpm': max(1500, min(2500, current.get('rpm', 2000) + random.randint(-100, 150))),
        'fuel_level': max(0, min(100, current.get('fuel_level', 80) + random.randint(-2, 1))),
        'coolant_temp': max(80, min(100, current.get('coolant_temp', 90) + random.randint(-2, 3)))
    }

# System activity logs generator
def generate_system_logs():
    """Generate realistic system activity logs"""
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
        f"[{current_time}] 💾 Backup Status: Last backup {random.randint(5, 25)} min ago",
        f"[{current_time}] 🔧 Maintenance Mode: Disabled - All services running",
        f"[{current_time}] 📈 Performance Monitor: CPU {random.randint(12, 35)}% | RAM {random.randint(45, 70)}%"
    ]
    
    return random.sample(log_messages, 6)  # Return 6 random log entries

# Page configuration
st.set_page_config(
    page_title="Route-Rakshak | Logistics Super-App",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .role-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c5aa0;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f4e79;
    }
    .tab-content {
        padding: 2rem;
        background-color: #fafafa;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .ai-result {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to execute AI tools directly (bypassing CrewAI crew to avoid OpenAI)
def execute_ai_task_direct(tool_name, input_data):
    """Execute AI tools directly without CrewAI crew to avoid OpenAI dependencies"""
    try:
        from tools import (
            drowsiness_detection_tool,
            engine_diagnosis_tool,
            market_search_tool,
            expense_validator_tool
        )
        
        # Map tool names to actual tools
        tool_map = {
            'safety': drowsiness_detection_tool,
            'engine': engine_diagnosis_tool,
            'market': market_search_tool,
            'expense': expense_validator_tool
        }
        
        if tool_name not in tool_map:
            return f"Unknown tool: {tool_name}", False
        
        # Execute the tool directly
        tool = tool_map[tool_name]
        
        if tool_name == 'safety':
            result = tool.run(input_data)
        elif tool_name == 'engine':
            result = tool.run(input_data)
        elif tool_name == 'market':
            result = tool.run(input_data)
        elif tool_name == 'expense':
            # For expense tool, input_data should be a dict with amount, item, category
            result = tool.run(**input_data)
        
        return str(result), True
        
    except Exception as e:
        return f"Tool Error: {str(e)}", False

# Main header
st.markdown('<h1 class="main-header">🚛 Route-Rakshak Logistics Super-App</h1>', unsafe_allow_html=True)

# Sidebar for role selection
with st.sidebar:
    st.markdown("### 🎯 Select Your Role")
    selected_role = st.selectbox(
        "Choose your role:",
        ["�‍✈️ Driver", "💼 Owner", "📦 Customer"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.metric("Active Vehicles", "24")
    st.metric("Today's Deliveries", "156")
    st.metric("Revenue Today", "₹45,230")
    
    # Live System Activity Logs
    st.markdown("---")
    with st.expander("📟 System Activity Logs", expanded=True):
        st.markdown("**🔴 LIVE SYSTEM STATUS**")
        
        # Generate and display system logs
        logs = generate_system_logs()
        for log in logs:
            st.text(log)
        
        # Auto-refresh button for logs
        if st.button("🔄 Refresh Logs", use_container_width=True):
            st.rerun()
        
        # System status indicators
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("🟢 **All Systems Online**")
        with col_s2:
            st.markdown(f"⏰ **{datetime.datetime.now().strftime('%H:%M:%S')}**")

# Main content area based on selected role
if selected_role == "�‍✈️ Driver":
    st.markdown('<h2 class="role-header">�‍✈️ Driver Dashboard</h2>', unsafe_allow_html=True)
    
    # Create tabs for driver workflow
    tab1, tab2, tab3 = st.tabs(["🚀 Start Trip", "🛣️ On Road", "🏁 End Trip"])
    
    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("### 🚀 Start Your Trip")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**� Trip Details**")
            st.write("• Vehicle ID: TN-01-AB-1234")
            st.write("• Route: Chennai → Bangalore")
            st.write("• Distance: 346 km")
            st.write("• Estimated Time: 6h 30m")
        
        with col2:
            st.markdown("**� Cargo Information**")
            st.write("• Total Packages: 25")
            st.write("• Weight: 2.5 tons")
            st.write("• Priority Deliveries: 3")
            st.write("• Fragile Items: 5")
        
        # AI-Powered Safety Check
        st.markdown("### 🤖 AI Safety Check")
        st.write("Upload a selfie for drowsiness detection before starting your trip:")
        
        uploaded_file = st.file_uploader("📸 Upload Driver Selfie", type=['jpg', 'jpeg', 'png'])
        
        if st.button("🔍 AI Safety Analysis", type="primary", use_container_width=True):
            if uploaded_file:
                with st.spinner('🤖 AI Safety Officer is analyzing your selfie...'):
                    # Execute AI safety check directly
                    result, success = execute_ai_task_direct('safety', uploaded_file.name)
                    
                    if success:
                        if "Safe" in result:
                            st.success(f"✅ **Safety Check Passed**\n\n{result}")
                        else:
                            st.error(f"⚠️ **Safety Alert**\n\n{result}")
                    else:
                        st.error(f"❌ Safety check failed: {result}")
            else:
                st.warning("Please upload a selfie first!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("### 🛣️ Trip in Progress")
        
        # Live Weather Widget
        st.markdown("### 🌤️ Live Weather Conditions")
        col_w1, col_w2 = st.columns([2, 1])
        
        with col_w1:
            # Get current truck location for weather
            truck_location = st.session_state['truck_location']
            weather_data = get_live_weather(truck_location['lat'], truck_location['lon'], truck_location['city'])
            
            st.markdown(f"""
            **📍 {weather_data['city']} Weather ({weather_data['status']})**
            
            {weather_data['emoji']} **{weather_data['temperature']}°C** | 💨 **{weather_data['windspeed']} km/h**
            """)
            
            # Weather status indicator
            if weather_data['success']:
                st.success("🌐 Live weather data from Open-Meteo API")
            else:
                st.info("📡 Using simulated weather data")
        
        with col_w2:
            if st.button("🔄 Refresh Weather", use_container_width=True):
                st.rerun()
        
        # Trip metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Speed", "65 km/h", "↗️ +5")
        with col2:
            st.metric("Distance Covered", "156 km", "45%")
        with col3:
            st.metric("ETA", "4h 15m", "⏰ On Time")
        
        st.markdown("**🗺️ Live Route Map**")
        st.info("� Current Location: Hosur Toll Plaza")
        
        # AI-Powered Engine Diagnosis
        st.markdown("### � AI Engine Diagnosis")
        st.write("Record engine sound for AI-powered mechanical analysis:")
        
        # Live IoT Sensor Readings
        st.markdown("**📊 Live Engine Sensors**")
        sensors = get_engine_sensors()
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("🌡️ Engine Temp", f"{sensors['engine_temp']}°C", 
                     "🟢 Normal" if sensors['engine_temp'] < 85 else "🟡 Warm")
            st.metric("⚡ Battery", f"{sensors['battery_voltage']}V",
                     "🟢 Good" if sensors['battery_voltage'] > 13.8 else "🟡 Low")
        
        with col_s2:
            st.metric("🛢️ Oil Pressure", f"{sensors['oil_pressure']} PSI",
                     "🟢 Normal" if sensors['oil_pressure'] > 35 else "🔴 Low")
            st.metric("⚙️ RPM", f"{sensors['rpm']}", 
                     "🟢 Optimal" if 1800 <= sensors['rpm'] <= 2200 else "🟡 Variable")
        
        with col_s3:
            st.metric("⛽ Fuel Level", f"{sensors['fuel_level']}%",
                     "🟢 Good" if sensors['fuel_level'] > 25 else "🟡 Low")
            st.metric("❄️ Coolant", f"{sensors['coolant_temp']}°C",
                     "🟢 Normal" if sensors['coolant_temp'] < 95 else "🟡 Warm")
        
        # Sensor refresh button
        if st.button("🔄 Refresh Sensors", type="secondary", use_container_width=True):
            refresh_engine_sensors()
            st.success("🔄 Sensor readings updated!")
            st.rerun()
        
        audio_file = st.file_uploader("🎵 Upload Engine Audio", type=['wav', 'mp3', 'm4a'])
        
        if st.button("🔍 AI Engine Analysis", type="secondary", use_container_width=True):
            if audio_file:
                with st.spinner('🤖 AI Mechanic is analyzing engine sounds...'):
                    # Execute AI engine diagnosis directly
                    result, success = execute_ai_task_direct('engine', audio_file.name)
                    
                    if success:
                        if "Healthy" in result:
                            st.success(f"✅ **Engine Status: Healthy**\n\n{result}")
                        elif "Issue" in result or "Critical" in result:
                            st.error(f"🚨 **Engine Alert**\n\n{result}")
                        else:
                            st.warning(f"⚠️ **Maintenance Needed**\n\n{result}")
                    else:
                        st.error(f"❌ Engine diagnosis failed: {result}")
            else:
                st.warning("Please upload an engine audio recording first!")
        
        # AI-Powered Expense Validation
        st.markdown("### � AI Expense Validator")
        col1, col2, col3 = st.columns(3)
        with col1:
            expense_amount = st.number_input("Amount (₹)", min_value=0.0, value=1500.0, step=100.0)
        with col2:
            expense_item = st.text_input("Expense Item", value="Fuel")
        with col3:
            expense_category = st.selectbox("Category", ["Fuel", "Food", "Maintenance", "Toll", "Parking", "General"])
        
        if st.button("🤖 AI Expense Validation", type="secondary", use_container_width=True):
            with st.spinner('🤖 AI Finance Manager is validating your expense...'):
                # Execute AI expense validation directly
                expense_data = {
                    'amount': expense_amount,
                    'item': expense_item,
                    'category': expense_category
                }
                result, success = execute_ai_task_direct('expense', expense_data)
                
                if success:
                    if "Approved" in result:
                        st.success(f"✅ **Expense Approved**\n\n{result}")
                    elif "Rejected" in result:
                        st.error(f"❌ **Expense Rejected**\n\n{result}")
                    else:
                        st.warning(f"⚠️ **Manual Review Required**\n\n{result}")
                else:
                    st.error(f"❌ Expense validation failed: {result}")
        
        # Fuel Theft Detection Calculator
        st.markdown("### ⛽ AI Fuel Theft Detection")
        st.write("Monitor fuel efficiency and detect potential theft incidents:")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            fuel_consumed = st.number_input("Fuel Consumed (Liters)", min_value=0.0, value=28.5, step=0.5)
        with col_f2:
            distance_traveled = st.number_input("Distance Traveled (km)", min_value=0.0, value=95.0, step=1.0)
        with col_f3:
            expected_mileage = st.number_input("Expected Mileage (km/l)", min_value=0.0, value=4.2, step=0.1)
        
        if st.button("🔍 Analyze Fuel Efficiency", type="secondary", use_container_width=True):
            if fuel_consumed > 0 and distance_traveled > 0:
                # Calculate actual mileage
                actual_mileage = distance_traveled / fuel_consumed
                efficiency_percentage = (actual_mileage / expected_mileage) * 100
                
                # Fuel theft detection logic (mileage < 3.5 km/l triggers theft alert)
                if actual_mileage < 3.5:
                    st.error(f"🚨 **FUEL THEFT ALERT DETECTED!**\n\n"
                            f"• Actual Mileage: {actual_mileage:.2f} km/l\n"
                            f"• Expected Mileage: {expected_mileage:.2f} km/l\n"
                            f"• Efficiency: {efficiency_percentage:.1f}%\n"
                            f"• **Status:** Critical - Possible fuel theft\n"
                            f"• **Action Required:** Immediate investigation needed\n\n"
                            f"**📋 Recommendations:**\n"
                            f"• Check fuel tank for tampering\n"
                            f"• Verify fuel receipts and records\n"
                            f"• Contact fleet manager immediately\n"
                            f"• Schedule vehicle inspection")
                elif actual_mileage < expected_mileage * 0.85:  # 15% below expected
                    st.warning(f"⚠️ **LOW FUEL EFFICIENCY WARNING**\n\n"
                              f"• Actual Mileage: {actual_mileage:.2f} km/l\n"
                              f"• Expected Mileage: {expected_mileage:.2f} km/l\n"
                              f"• Efficiency: {efficiency_percentage:.1f}%\n"
                              f"• **Status:** Below optimal performance\n\n"
                              f"**📋 Possible Causes:**\n"
                              f"• Heavy traffic conditions\n"
                              f"• Vehicle maintenance needed\n"
                              f"• Driving pattern optimization required\n"
                              f"• Minor fuel system issues")
                else:
                    st.success(f"✅ **FUEL EFFICIENCY NORMAL**\n\n"
                              f"• Actual Mileage: {actual_mileage:.2f} km/l\n"
                              f"• Expected Mileage: {expected_mileage:.2f} km/l\n"
                              f"• Efficiency: {efficiency_percentage:.1f}%\n"
                              f"• **Status:** Optimal performance\n"
                              f"• **Fuel Security:** No theft indicators detected")
                
                # Additional fuel monitoring metrics
                fuel_cost_per_km = (fuel_consumed / distance_traveled) * 85  # Assuming ₹85 per liter
                total_fuel_cost = fuel_consumed * 85
                
                st.info(f"💰 **FUEL COST ANALYSIS:**\n"
                       f"• Total Fuel Cost: ₹{total_fuel_cost:,.2f}\n"
                       f"• Cost per km: ₹{fuel_cost_per_km:.2f}\n"
                       f"• Fuel Consumed: {fuel_consumed} liters\n"
                       f"• Distance Covered: {distance_traveled} km")
            else:
                st.warning("Please enter valid fuel and distance values!")
        
        st.markdown("**� Emergency Contacts**")
        st.write("• Fleet Manager: +91 98765 43210")
        st.write("• Emergency Helpline: 1800-ROUTE-911")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("### 🏁 Complete Trip")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Trip Summary**")
            st.write("• Total Distance: 346 km")
            st.write("• Total Time: 6h 25m")
            st.write("• Fuel Consumed: 28 liters")
            st.write("• Packages Delivered: 25/25")
        
        with col2:
            st.markdown("**� Earnings**")
            st.write("• Base Pay: ₹2,500")
            st.write("• Distance Bonus: ₹346")
            st.write("• On-time Bonus: ₹200")
            st.write("• **Total: ₹3,046**")
        
        # AI-Powered Return Load Search
        st.markdown("### � AI Return Load Finder")
        st.write("Find profitable return loads to maximize your earnings:")
        
        current_location = st.text_input("Current Location", value="Bangalore")
        
        if st.button("🤖 Find Return Loads", type="primary", use_container_width=True):
            with st.spinner('🤖 AI Logistics Manager is searching for profitable return loads...'):
                # Execute AI return load search directly
                result, success = execute_ai_task_direct('market', current_location)
                
                if success:
                    st.success("🎯 **Return Load Opportunities Found!**")
                    st.markdown(f'<div class="ai-result">{result}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Return load search failed: {result}")
        
        if st.button("🏁 Complete Trip", type="secondary", use_container_width=True):
            st.success("✅ Trip completed successfully! Safe travels!")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif selected_role == "💼 Owner":
    st.markdown('<h2 class="role-header">💼 Fleet Owner Dashboard</h2>', unsafe_allow_html=True)
    
    # Create two columns for owner dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚛 Fleet Overview")
        
        # Fleet metrics from session state
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        metrics = st.session_state['fleet_metrics']
        with metric_col1:
            st.metric("Total Vehicles", metrics['total_vehicles'], "+2")
        with metric_col2:
            st.metric("Active Trips", metrics['active_trips'], "+5")
        with metric_col3:
            st.metric("Available", metrics['available'], "-3")
        with metric_col4:
            st.metric("In Maintenance", metrics['in_maintenance'], "0")
        
        # Sample fleet data
        fleet_data = pd.DataFrame(st.session_state['fleet_data'])
        
        st.dataframe(fleet_data, use_container_width=True)
        
        # Enhanced Revenue vs Expense Chart
        st.markdown("### 📊 Weekly Income vs Expense Analysis")
        
        # Create comprehensive financial data from session state
        financial_data = pd.DataFrame(st.session_state['financial_data'])
        
        # Display the chart
        st.bar_chart(financial_data.set_index('Day')[['Income', 'Expense', 'Profit']], use_container_width=True)
        
        # Profit summary metrics
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            total_income = financial_data['Income'].sum()
            st.metric("Weekly Income", f"₹{total_income:,}", "+12%")
        with col_p2:
            total_expense = financial_data['Expense'].sum()
            st.metric("Weekly Expense", f"₹{total_expense:,}", "+8%")
        with col_p3:
            total_profit = financial_data['Profit'].sum()
            st.metric("Weekly Profit", f"₹{total_profit:,}", "+18%")
        
        # Fleet Status Visualization (Dynamic)
        st.markdown("### 🚛 Fleet Status Distribution")
        
        # Calculate dynamic fleet status from session state
        fleet_data = st.session_state['fleet_data']
        active_count = len([v for v in fleet_data if '🛣️' in v['Status']])
        starting_count = len([v for v in fleet_data if '🚀' in v['Status']])
        completed_count = len([v for v in fleet_data if '🏁' in v['Status']])
        maintenance_count = len([v for v in fleet_data if '🔧' in v['Status']])
        
        # Fleet status data
        fleet_status_data = pd.DataFrame({
            'Status': ['Active', 'Starting', 'Completed', 'Maintenance'],
            'Count': [active_count, starting_count, completed_count, maintenance_count],
        })
        
        # Display fleet status as metrics and chart
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            st.metric("� Active", active_count, "+3")
        with col_f2:
            st.metric("� Starting", starting_count, "-2")
        with col_f3:
            st.metric("🟡 Completed", completed_count, "+1")
        with col_f4:
            st.metric("🔴 Maintenance", maintenance_count, "0")
        
        # Fleet efficiency chart
        if fleet_status_data['Count'].sum() > 0:  # Only show chart if there's data
            st.bar_chart(fleet_status_data.set_index('Status')['Count'], use_container_width=True)
    
    with col2:
        st.markdown("### 🚨 Alerts & Notifications")
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**🔴 High Priority**")
        st.write("• Vehicle TN-05-IJ-7890 - Engine warning")
        st.write("• Driver late for pickup - Route 15")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**🟡 Medium Priority**")
        st.write("• Fuel prices increased by 3%")
        st.write("• 2 vehicles due for service")
        st.write("• New delivery request - Coimbatore")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**🟢 Low Priority**")
        st.write("• Driver performance report ready")
        st.write("• Monthly insurance renewal due")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Quick Actions")
        
        # Interactive Add New Vehicle Form
        with st.form("add_vehicle_form"):
            st.markdown("**➕ Add New Vehicle**")
            col_v1, col_v2 = st.columns(2)
            
            with col_v1:
                new_vehicle_id = st.text_input("Vehicle ID", placeholder="e.g., TN-05-XY-9876")
                new_driver_name = st.text_input("Driver Name", placeholder="e.g., Ramesh Kumar")
            
            with col_v2:
                new_route = st.text_input("Route", placeholder="e.g., Chennai → Coimbatore")
                new_status = st.selectbox("Status", ["🚀 Starting", "🛣️ On Road", "🏁 Completed", "🔧 Maintenance"])
            
            new_eta = st.text_input("ETA", placeholder="e.g., 3h 30m")
            
            submitted = st.form_submit_button("🚛 Add Vehicle to Fleet", use_container_width=True)
            
            if submitted:
                if new_vehicle_id and new_driver_name and new_route:
                    # Add new vehicle to session state
                    new_vehicle = {
                        'Vehicle ID': new_vehicle_id,
                        'Driver': new_driver_name,
                        'Route': new_route,
                        'Status': new_status,
                        'ETA': new_eta if new_eta else "TBD"
                    }
                    
                    st.session_state['fleet_data'].append(new_vehicle)
                    
                    # Update fleet metrics
                    st.session_state['fleet_metrics']['total_vehicles'] = len(st.session_state['fleet_data'])
                    st.session_state['fleet_metrics']['active_trips'] = len([v for v in st.session_state['fleet_data'] if '🛣️' in v['Status']])
                    st.session_state['fleet_metrics']['available'] = len([v for v in st.session_state['fleet_data'] if '🚀' in v['Status']])
                    st.session_state['fleet_metrics']['completed'] = len([v for v in st.session_state['fleet_data'] if '🏁' in v['Status']])
                    st.session_state['fleet_metrics']['in_maintenance'] = len([v for v in st.session_state['fleet_data'] if '🔧' in v['Status']])
                    
                    st.success(f"✅ Vehicle {new_vehicle_id} added to fleet successfully!")
                    st.balloons()  # Celebration effect
                    st.rerun()  # Refresh the app to show new data
                else:
                    st.error("❌ Please fill in Vehicle ID, Driver Name, and Route fields!")
        
        # Other quick actions
        if st.button("👥 Manage Drivers"):
            st.info("📋 Driver management panel opened!")
        if st.button("📋 Generate Report"):
            st.success("📊 Generating comprehensive fleet report...")
        if st.button("⚙️ Settings"):
            st.info("⚙️ Settings panel opened!")
        
        # Load Optimization Calculator
        st.markdown("### ⚖️ Load Optimization Calculator")
        st.write("Calculate optimal truck allocation for cargo loads:")
        
        cargo_weight = st.number_input("Enter Total Cargo Weight (Tons)", min_value=0.0, max_value=50.0, value=8.5, step=0.5)
        
        if st.button("🧮 Calculate Load Distribution"):
            if cargo_weight <= 10:
                st.success(f"✅ **Standard Truck Sufficient**\n\n"
                          f"• Cargo Weight: {cargo_weight} tons\n"
                          f"• Truck Capacity: 10 tons\n"
                          f"• Remaining Capacity: {10 - cargo_weight} tons\n"
                          f"• **Recommendation:** Use 1 Standard Truck")
            else:
                remaining_weight = cargo_weight - 10
                st.warning(f"⚠️ **Overload Detected!**\n\n"
                          f"• Total Cargo: {cargo_weight} tons\n"
                          f"• Standard Truck Limit: 10 tons\n"
                          f"• Excess Weight: {remaining_weight} tons\n\n"
                          f"**📋 Recommendation:**\n"
                          f"• Book 1 Standard Truck (10 tons)\n"
                          f"• Book 1 'Chota Hathi' Tempo ({remaining_weight} tons)\n"
                          f"• **Total Vehicles Required:** 2")
                
                # Cost calculation
                standard_cost = 10000  # Base cost for standard truck
                tempo_cost = remaining_weight * 800  # Cost per ton for tempo
                total_cost = standard_cost + tempo_cost
                
                st.info(f"💰 **Cost Estimation:**\n"
                       f"• Standard Truck: ₹{standard_cost:,}\n"
                       f"• Tempo ({remaining_weight}T): ₹{tempo_cost:,}\n"
                       f"• **Total Cost:** ₹{total_cost:,}")
        
        # Fleet Utilization Insights
        st.markdown("### 📈 Fleet Utilization Insights")
        utilization_data = pd.DataFrame({
            'Metric': ['Avg Load Factor', 'Route Efficiency', 'Fuel Efficiency', 'Driver Performance'],
            'Current': [78, 85, 72, 88],
            'Target': [85, 90, 80, 90],
            'Status': ['🟡 Needs Improvement', '🟢 Good', '🟡 Needs Improvement', '🟢 Excellent']
        })
        st.dataframe(utilization_data, use_container_width=True)

elif selected_role == "📦 Customer":
    st.markdown('<h2 class="role-header">📦 Customer Tracking Portal</h2>', unsafe_allow_html=True)
    
    # Customer tracking interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🗺️ Live Tracking Map")
        
        # Real-time GPS simulation controls
        col_gps1, col_gps2 = st.columns([3, 1])
        
        with col_gps2:
            st.markdown("**📡 GPS Controls**")
            
            # Live Tracking Toggle
            if not st.session_state.get('live_tracking_active', False):
                if st.button("🔴 Start Live Tracking", use_container_width=True):
                    st.session_state['live_tracking_active'] = True
                    st.success("🔴 Live tracking started! Truck will move automatically...")
                    st.rerun()
            else:
                if st.button("⏹️ Stop Live Tracking", use_container_width=True):
                    st.session_state['live_tracking_active'] = False
                    st.info("⏹️ Live tracking stopped.")
                    st.rerun()
            
            # Auto-movement logic when live tracking is active
            if st.session_state.get('live_tracking_active', False):
                current_index = st.session_state.get('truck_index', 0)
                route_coords = st.session_state['route_coordinates']
                
                if current_index < len(route_coords) - 1:
                    # Move to next position
                    import time
                    time.sleep(1)  # Wait 1 second
                    
                    next_index = current_index + 1
                    st.session_state['truck_index'] = next_index
                    st.session_state['truck_location'] = route_coords[next_index].copy()
                    
                    st.success(f"🚛 Truck moved to {route_coords[next_index]['city']} ({route_coords[next_index]['progress']}%)")
                    st.rerun()  # Refresh to show movement
                else:
                    # Journey completed
                    st.session_state['live_tracking_active'] = False
                    st.balloons()
                    st.success("🏁 Journey completed! Truck has reached Pune!")
            
            # Manual movement button
            if st.button("� Manual Step Forward", use_container_width=True):
                current_index = st.session_state.get('truck_index', 0)
                route_coords = st.session_state['route_coordinates']
                
                if current_index < len(route_coords) - 1:
                    next_index = current_index + 1
                    st.session_state['truck_index'] = next_index
                    st.session_state['truck_location'] = route_coords[next_index].copy()
                    st.success(f"🚛 Truck moved to {route_coords[next_index]['city']} ({route_coords[next_index]['progress']}%)")
                    st.rerun()
                else:
                    st.info("🏁 Truck has reached destination!")
            
            if st.button("🔄 Reset Journey", use_container_width=True):
                # Reset truck to starting position
                st.session_state['truck_location'] = st.session_state['route_coordinates'][0].copy()
                st.session_state['truck_index'] = 0
                st.session_state['live_tracking_active'] = False
                st.success("🔄 Journey reset to Nagpur!")
                st.rerun()
            
            # Show current status
            current_location = st.session_state['truck_location']
            st.metric("Journey Progress", f"{current_location['progress']}%")
            st.write(f"📍 Current: {current_location['city']}")
            
            # Live tracking status indicator
            if st.session_state.get('live_tracking_active', False):
                st.markdown("🔴 **LIVE TRACKING ACTIVE**")
            else:
                st.markdown("⚪ **TRACKING PAUSED**")
        
        with col_gps1:
            # Create interactive folium map with real-time truck location
            # Center the map on Maharashtra (between Nagpur and Pune)
            center_lat, center_lon = 20.0, 76.0
            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=7,
                tiles='OpenStreetMap'
            )
            
            # Define route coordinates
            nagpur = [21.1458, 79.0882]  # Origin
            pune = [18.5204, 73.8567]    # Destination
            
            # Get current truck location from session state
            truck_location = [st.session_state['truck_location']['lat'], st.session_state['truck_location']['lon']]
            
            # Add route line (Red polyline from Nagpur to Pune)
            route_coordinates = [nagpur, truck_location, pune]
            folium.PolyLine(
                locations=route_coordinates,
                color='red',
                weight=4,
                opacity=0.8,
                popup='🚛 Delivery Route: Nagpur → Pune'
            ).add_to(m)
            
            # Add origin marker (Nagpur)
            folium.Marker(
                location=nagpur,
                popup='📦 Origin: Nagpur Warehouse<br>Pickup Time: 10:30 AM',
                tooltip='Nagpur - Origin',
                icon=folium.Icon(color='green', icon='play')
            ).add_to(m)
            
            # Add destination marker (Pune)
            folium.Marker(
                location=pune,
                popup='🏠 Destination: Pune<br>Expected: 6:30 PM',
                tooltip='Pune - Destination',
                icon=folium.Icon(color='blue', icon='stop')
            ).add_to(m)
            
            # Add current truck location marker (REAL-TIME)
            folium.Marker(
                location=truck_location,
                popup=f'🚛 MH-31 Truck ({st.session_state["truck_location"]["progress"]}% Complete)<br>Location: {st.session_state["truck_location"]["city"]}<br>Driver: Raj Kumar<br>Speed: 65 km/h',
                tooltip=f'Current Location - {st.session_state["truck_location"]["city"]}',
                icon=folium.Icon(color='red', icon='truck', prefix='fa')
            ).add_to(m)
            
            # Add some intermediate checkpoints
            checkpoints = [
                ([20.7, 78.1], '✅ Checkpoint 1: Wardha (Completed)'),
                ([19.8, 75.3], '🔄 Checkpoint 2: Ahmednagar (In Transit)'),
                ([19.2, 74.2], '⏳ Checkpoint 3: Pune Outskirts (Pending)')
            ]
            
            for i, (location, popup_text) in enumerate(checkpoints):
                color = 'green' if i == 0 else 'orange' if i == 1 else 'gray'
                folium.CircleMarker(
                    location=location,
                    radius=8,
                    popup=popup_text,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(m)
            
            # Display the interactive map
            st_folium(m, height=500, use_container_width=True)
        
        # Live tracking status (dynamic based on truck location)
        st.markdown("### 📊 Live Tracking Status")
        col_a, col_b, col_c = st.columns(3)
        
        progress = st.session_state['truck_location']['progress']
        distance_covered = int(346 * progress / 100)  # Total route is 346 km
        remaining_distance = 346 - distance_covered
        
        with col_a:
            st.metric("Distance Covered", f"{distance_covered} km", f"{progress}%")
        with col_b:
            current_speed = 65 if progress < 100 else 0
            speed_status = "🔴 LIVE" if st.session_state.get('live_tracking_active', False) else "⏸️ Paused"
            st.metric("Current Speed", f"{current_speed} km/h", speed_status)
        with col_c:
            if progress < 100:
                eta_hours = remaining_distance / 65  # Assuming 65 km/h average speed
                eta_text = f"{eta_hours:.1f}h remaining"
            else:
                eta_text = "🏁 Arrived"
            st.metric("ETA", eta_text, "⏰ On Time")
        
        # Delivery timeline (dynamic based on progress)
        st.markdown("### 📋 Delivery Timeline")
        
        progress = st.session_state['truck_location']['progress']
        current_city = st.session_state['truck_location']['city']
        
        # Dynamic timeline based on progress
        if progress == 0:
            timeline_data = pd.DataFrame({
                'Status': ['📦 Order Placed', '✅ Picked Up', '🚛 In Transit', '🏠 Out for Delivery', '✅ Delivered'],
                'Time': ['10:30 AM', '11:15 AM', 'Pending', 'Pending', 'Pending'],
                'Location': ['Nagpur Warehouse', 'Nagpur Hub', 'En Route', 'Pune Hub', 'Your Address'],
                'Completed': ['✅', '✅', '⏳', '⏳', '⏳']
            })
        elif progress < 50:
            timeline_data = pd.DataFrame({
                'Status': ['📦 Order Placed', '✅ Picked Up', '🚛 In Transit', '🏠 Out for Delivery', '✅ Delivered'],
                'Time': ['10:30 AM', '11:15 AM', '2:45 PM', 'Pending', 'Pending'],
                'Location': ['Nagpur Warehouse', 'Nagpur Hub', f'{current_city} (Current)', 'Pune Hub', 'Your Address'],
                'Completed': ['✅', '✅', '🔄', '⏳', '⏳']
            })
        elif progress < 100:
            timeline_data = pd.DataFrame({
                'Status': ['📦 Order Placed', '✅ Picked Up', '🚛 In Transit', '🏠 Out for Delivery', '✅ Delivered'],
                'Time': ['10:30 AM', '11:15 AM', '2:45 PM', '5:30 PM', 'Pending'],
                'Location': ['Nagpur Warehouse', 'Nagpur Hub', 'Completed', f'{current_city} (Current)', 'Your Address'],
                'Completed': ['✅', '✅', '✅', '🔄', '⏳']
            })
        else:
            timeline_data = pd.DataFrame({
                'Status': ['📦 Order Placed', '✅ Picked Up', '🚛 In Transit', '🏠 Out for Delivery', '✅ Delivered'],
                'Time': ['10:30 AM', '11:15 AM', '2:45 PM', '5:30 PM', '6:15 PM'],
                'Location': ['Nagpur Warehouse', 'Nagpur Hub', 'Completed', 'Completed', 'Delivered Successfully!'],
                'Completed': ['✅', '✅', '✅', '✅', '✅']
            })
        
        st.dataframe(timeline_data, use_container_width=True)
    
    with col2:
        st.markdown("### 📦 Package Details")
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**📋 Order Information**")
        st.write("• **Tracking ID:** RR-2024-001234")
        st.write("• **Order Date:** Jan 30, 2024")
        st.write("• **Expected Delivery:** Jan 31, 2024")
        st.write("• **Package Weight:** 2.5 kg")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**🚛 Vehicle Details**")
        st.write("• **Vehicle:** TN-01-AB-1234")
        st.write("• **Driver:** Raj Kumar")
        st.write("• **Contact:** +91 98765 43210")
        st.write("• **Current Speed:** 65 km/h")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**📍 Delivery Address**")
        st.write("• **Name:** John Doe")
        st.write("• **Address:** 123, MG Road")
        st.write("• **City:** Bangalore, KA")
        st.write("• **PIN:** 560001")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Customer actions
        st.markdown("### 📞 Quick Actions")
        if st.button("📞 Call Driver"):
            st.success("📞 Connecting to driver Raj Kumar...")
        if st.button("📧 Send Message"):
            st.info("📧 Message composer opened!")
        if st.button("📋 Delivery Instructions"):
            st.info("📋 Delivery instructions form opened!")
        if st.button("❌ Cancel Order"):
            st.warning("⚠️ Order cancellation requires confirmation!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🚛 Route-Rakshak © 2024 | Powered by AI & Innovation | CrewAI + Groq Integration"
    "</div>", 
    unsafe_allow_html=True
)