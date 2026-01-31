# 🚀 Route-Rakshak Startup Guide

Complete guide to run the Route-Rakshak Logistics Super-App with React frontend and FastAPI backend.

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- Internet connection (for OpenStreetMap tiles and weather API)

## 🔧 Initial Setup (One-Time)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create/verify `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com/

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

## 🏃 Running the Application

You need to run **TWO servers** simultaneously:

### Terminal 1: Start Backend (FastAPI)

```bash
cd backend
python start.py
```

**Backend will run on:** http://localhost:8000

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend (React)

```bash
cd frontend
npm run dev
```

**Frontend will run on:** http://localhost:5173

You should see:
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

## 🌐 Access the Application

Open your browser and navigate to:

**http://localhost:5173**

## 🎯 Features to Test

### 1. Driver Dashboard
- Click "Find Loads" to search for return loads
- Click "Check Safety" for AI drowsiness detection
- Click "Diagnose Engine" for engine sound analysis
- Click "Validate Expense" to verify expenses
- Click "Refresh" on IoT sensors to see live data changes
- View live weather data for Nagpur

### 2. Fleet Owner Dashboard
- Click "Add Vehicle" to add new trucks to the fleet
- View real-time fleet metrics (Total, Active, Available, Completed)
- See weekly income vs expense chart
- Monitor all vehicles in the fleet table

### 3. Customer Dashboard
- Click "Start Live Tracking" to auto-animate truck movement
- Click "Manual Step" to move truck one waypoint forward
- Click "Reset" to restart journey from Nagpur
- View live tracking status (distance, speed, ETA)
- See package and vehicle details

## 🔍 API Endpoints (Backend)

The FastAPI backend exposes these endpoints:

### AI Agent Endpoints
- `POST /api/find-load` - Find return loads
- `POST /api/check-safety` - Drowsiness detection
- `POST /api/diagnose-engine` - Engine diagnosis
- `POST /api/validate-expense` - Expense validation

### Truck Location Endpoints
- `GET /api/truck-location` - Get current location
- `POST /api/truck-location/move` - Move truck forward
- `POST /api/truck-location/reset` - Reset to start
- `POST /api/truck-location/toggle-tracking` - Start/stop auto-tracking

### Fleet Management Endpoints
- `GET /api/fleet` - Get all vehicles
- `POST /api/fleet/add` - Add new vehicle

### IoT & Data Endpoints
- `GET /api/sensors` - Get sensor readings
- `POST /api/sensors/refresh` - Refresh sensors
- `GET /api/weather` - Get live weather
- `GET /api/system-logs` - Get system logs

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`
**Solution:**
```bash
pip install -r requirements.txt
```

**Problem:** `GROQ_API_KEY not found`
**Solution:** Add your Groq API key to `.env` file

**Problem:** Port 8000 already in use
**Solution:** Kill the process using port 8000 or change port in `backend/start.py`

### Frontend Issues

**Problem:** `npm: command not found`
**Solution:** Install Node.js from https://nodejs.org/

**Problem:** Dependencies not installed
**Solution:**
```bash
cd frontend
npm install
```

**Problem:** Map not loading
**Solution:** Check internet connection (OpenStreetMap requires internet)

**Problem:** API calls failing
**Solution:** Ensure backend is running on port 8000

### CORS Issues

If you see CORS errors in browser console:
1. Verify backend CORS settings in `backend/main.py`
2. Check that frontend URL matches allowed origins
3. Restart both servers

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Browser (Port 5173)                   │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Driver     │  │ Fleet Owner  │  │  Customer    │ │
│  │  Dashboard   │  │  Dashboard   │  │  Dashboard   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│              React + Vite + Tailwind CSS                │
└─────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/REST API (Axios)
                           ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                 │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  AI Agents   │  │   Fleet      │  │  IoT Data    │ │
│  │  (CrewAI)    │  │  Management  │  │  & Weather   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│              Python + FastAPI + Uvicorn                 │
└─────────────────────────────────────────────────────────┘
                           │
                           │ API Calls
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   External Services                      │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Groq API    │  │  Open-Meteo  │  │ OpenStreetMap│ │
│  │  (AI Model)  │  │  (Weather)   │  │  (Map Tiles) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 📝 Development Tips

### Hot Reload

Both servers support hot reload:
- **Backend:** Uvicorn auto-reloads on Python file changes
- **Frontend:** Vite auto-reloads on React file changes

### Debugging

**Backend Logs:** Check terminal running `python start.py`
**Frontend Logs:** Open browser DevTools Console (F12)
**API Testing:** Visit http://localhost:8000/docs for Swagger UI

### Code Structure

**Backend:**
- `backend/main.py` - FastAPI routes and endpoints
- `agents.py` - CrewAI agent definitions
- `tools.py` - Custom AI tools
- `tasks.py` - Agent tasks

**Frontend:**
- `frontend/src/App.jsx` - Main app with tab navigation
- `frontend/src/components/` - React components
- `frontend/src/services/api.js` - API service layer

## 🎉 Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can switch between Driver/Owner/Customer tabs
- [ ] AI tools respond with data
- [ ] Map displays with truck marker
- [ ] Live tracking animation works
- [ ] IoT sensors show fluctuating values
- [ ] Weather widget displays live data
- [ ] Fleet management allows adding vehicles

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs in Terminal 1
3. Check browser console for frontend errors
4. Verify all dependencies are installed

## 🚀 Next Steps

- Customize the UI styling in Tailwind CSS
- Add more AI agents and tools
- Integrate real GPS tracking hardware
- Deploy to production (Vercel for frontend, Railway for backend)
- Add authentication and user management
- Implement real-time WebSocket updates

---

**Happy Tracking! 🚛📦**
