# Route-Rakshak Frontend (React + Vite)

Modern React frontend for the Route-Rakshak Logistics Super-App with real-time tracking, AI-powered tools, and fleet management.

## 🚀 Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Leaflet** - OpenStreetMap integration
- **Recharts** - Data visualization
- **Axios** - API communication
- **Lucide React** - Icons

## 📦 Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## 🏃 Running the App

### Development Mode

Start the development server (runs on http://localhost:5173):
```bash
npm run dev
```

The app will automatically reload when you make changes.

### Production Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## 🔌 Backend Connection

The frontend connects to the FastAPI backend running on `http://localhost:8000`.

**Make sure the backend is running before starting the frontend:**

```bash
# In a separate terminal, navigate to backend directory
cd backend

# Start the FastAPI server
python start.py
```

## 🗺️ Features

### Driver Dashboard
- **AI Safety Check** - Drowsiness detection
- **Engine Diagnosis** - AI-powered sound analysis
- **Find Return Load** - Market search for available loads
- **Expense Validation** - AI expense verification
- **Live IoT Sensors** - Real-time engine monitoring
- **Weather Widget** - Live weather data

### Fleet Owner Dashboard
- **Fleet Management** - Add and track vehicles
- **Financial Analytics** - Income vs Expense charts
- **Fleet Overview** - Real-time vehicle status
- **Performance Metrics** - Active trips, available vehicles

### Customer Dashboard
- **Live Tracking Map** - OpenStreetMap with real-time truck location
- **Auto-Animation** - Truck moves automatically along route
- **Package Details** - Tracking ID, delivery info
- **Vehicle Details** - Driver contact, current location
- **Quick Actions** - Call driver, send message

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── DriverDashboard.jsx      # Driver interface
│   │   ├── OwnerDashboard.jsx       # Fleet management
│   │   ├── CustomerDashboard.jsx    # Live tracking
│   │   ├── MapComponent.jsx         # OpenStreetMap integration
│   │   ├── WeatherWidget.jsx        # Weather display
│   │   └── Sidebar.jsx              # System logs sidebar
│   ├── services/
│   │   └── api.js                   # API service layer
│   ├── App.jsx                      # Main app component
│   ├── main.jsx                     # React entry point
│   └── index.css                    # Global styles
├── index.html                       # HTML template
├── vite.config.js                   # Vite configuration
├── tailwind.config.js               # Tailwind CSS config
├── postcss.config.js                # PostCSS config
└── package.json                     # Dependencies
```

## 🔧 Configuration

### API Base URL

To change the backend URL, edit `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### Map Tiles

The app uses OpenStreetMap tiles. To use a different tile provider, edit `src/components/MapComponent.jsx`:

```javascript
<TileLayer
  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
  attribution='&copy; OpenStreetMap contributors'
/>
```

## 🐛 Troubleshooting

### Port Already in Use

If port 5173 is already in use, Vite will automatically try the next available port (5174, 5175, etc.).

### CORS Errors

Make sure the FastAPI backend has CORS enabled for `http://localhost:5173`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Map Not Loading

If the map doesn't load:
1. Check your internet connection (OpenStreetMap tiles require internet)
2. Ensure `leaflet` CSS is imported in `index.css`
3. Check browser console for errors

### API Connection Failed

If API calls fail:
1. Verify the backend is running on port 8000
2. Check the API_BASE_URL in `src/services/api.js`
3. Open browser DevTools Network tab to see failed requests

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📄 License

MIT License - Route-Rakshak Logistics Super-App
