# Route-Rakshak FastAPI Backend

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install fastapi uvicorn[standard] requests python-dotenv
```

### 2. Start the Backend Server
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or use the start script:
```bash
python backend/start.py
```

### 3. Access the API
- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## 📡 API Endpoints

### AI Agent Endpoints
- `POST /api/find-load` - Find return loads (Logistics Agent)
- `POST /api/check-safety` - Drowsiness detection (Safety Agent)
- `POST /api/diagnose-engine` - Engine diagnosis (Mechanic Agent)
- `POST /api/validate-expense` - Expense validation (Finance Agent)

### Truck Location & Tracking
- `GET /api/truck-location` - Get current truck GPS coordinates
- `POST /api/truck-location/move` - Move truck to next position
- `POST /api/truck-location/reset` - Reset truck to starting position
- `POST /api/truck-location/toggle-tracking` - Toggle live tracking

### Fleet Management
- `GET /api/fleet` - Get all fleet vehicles
- `POST /api/fleet/add` - Add new vehicle to fleet

### IoT & Monitoring
- `GET /api/sensors` - Get IoT sensor readings
- `POST /api/sensors/refresh` - Refresh sensor data
- `GET /api/weather` - Get live weather data
- `GET /api/system-logs` - Get system activity logs

## 🧪 Testing

Run the test suite:
```bash
python test_fastapi_backend.py
```

## 🔧 Configuration

The backend uses:
- **Port:** 8000
- **CORS:** Enabled for `http://localhost:3000` (React dev server)
- **Auto-reload:** Enabled for development

## 📦 Example API Calls

### Find Load
```bash
curl -X POST http://localhost:8000/api/find-load \
  -H "Content-Type: application/json" \
  -d '{"location": "Bangalore"}'
```

### Get Truck Location
```bash
curl http://localhost:8000/api/truck-location
```

### Get Sensors
```bash
curl http://localhost:8000/api/sensors
```

## 🎯 Next Steps

Once the backend is running, you can:
1. Test all endpoints using the interactive docs at `/docs`
2. Run the test suite to verify everything works
3. Start building the React frontend that connects to these APIs

## 🔗 Integration with React

The React frontend should use these base URLs:
- Development: `http://localhost:8000`
- Production: Update CORS settings in `main.py`

All endpoints return JSON responses with this structure:
```json
{
  "success": true,
  "data": {...},
  "timestamp": "2024-01-31T18:00:00"
}
```