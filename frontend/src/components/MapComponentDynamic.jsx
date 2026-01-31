import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import { getTruckLocation } from '../services/api';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom truck icon using DivIcon with emoji
const createTruckIcon = () => {
  return L.divIcon({
    html: '<div style="font-size: 30px; text-align: center; line-height: 1;">🚛</div>',
    className: 'custom-truck-icon',
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  });
};

// Component to handle map centering
const MapController = ({ center }) => {
  const map = useMap();
  
  useEffect(() => {
    if (center) {
      map.flyTo(center, map.getZoom(), {
        duration: 1.5,
        easeLinearity: 0.25
      });
    }
  }, [center, map]);
  
  return null;
};

const MapComponentDynamic = () => {
  const [truckLocation, setTruckLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const prevLocationRef = useRef(null);

  // Route coordinates
  const nagpur = [21.1458, 79.0882];
  const pune = [18.5204, 73.8567];

  // Fetch truck location
  const fetchTruckLocation = async () => {
    try {
      const data = await getTruckLocation();
      if (data.success) {
        prevLocationRef.current = truckLocation;
        setTruckLocation(data.location);
        setLastUpdate(new Date());
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching truck location:', error);
      setLoading(false);
    }
  };

  // Poll truck location every 1 second for smooth movement
  useEffect(() => {
    fetchTruckLocation();
    const interval = setInterval(fetchTruckLocation, 1000);
    return () => clearInterval(interval);
  }, []);

  if (loading || !truckLocation) {
    return (
      <div className="h-full flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600 mx-auto mb-4"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl">🗺️</span>
            </div>
          </div>
          <p className="text-gray-700 font-medium">Loading live map...</p>
          <p className="text-gray-500 text-sm mt-1">Connecting to GPS...</p>
        </div>
      </div>
    );
  }

  const currentPosition = [truckLocation.lat, truckLocation.lon];
  
  // Create smooth route line from Nagpur through current position to Pune
  const routeLine = [nagpur, currentPosition];
  const remainingRoute = [currentPosition, pune];

  return (
    <div className="h-full w-full rounded-lg overflow-hidden shadow-2xl relative">
      {/* Live Indicator - Enhanced */}
      <div className="absolute top-4 right-4 z-[1000] bg-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 border-2 border-red-500">
        <div className="relative flex items-center justify-center">
          <div className="w-4 h-4 bg-red-500 rounded-full animate-pulse"></div>
          <div className="absolute inset-0 w-4 h-4 bg-red-500 rounded-full animate-ping"></div>
        </div>
        <div>
          <div className="text-sm font-bold text-red-600">🔴 LIVE TRACKING</div>
          <div className="text-xs text-gray-500">
            Updated: {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
      </div>

      {/* Speed Indicator */}
      <div className="absolute top-20 right-4 z-[1000] bg-white px-4 py-2 rounded-lg shadow-lg">
        <div className="text-xs text-gray-500">Current Speed</div>
        <div className="text-lg font-bold text-blue-600">
          {truckLocation.progress < 100 ? '65 km/h' : '0 km/h'}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="absolute bottom-4 left-4 right-4 z-[1000] bg-white px-4 py-3 rounded-lg shadow-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-semibold text-gray-700">Journey Progress</span>
          <span className="text-sm font-bold text-blue-600">{truckLocation.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-green-500 to-blue-500 h-3 rounded-full transition-all duration-1000 ease-out relative"
            style={{ width: `${truckLocation.progress}%` }}
          >
            <div className="absolute inset-0 bg-white opacity-30 animate-pulse"></div>
          </div>
        </div>
        <div className="flex justify-between mt-2 text-xs text-gray-500">
          <span>📦 Nagpur</span>
          <span>📍 {truckLocation.city}</span>
          <span>🏠 Pune</span>
        </div>
      </div>
      
      <MapContainer
        center={[20.0, 76.0]}
        zoom={7}
        style={{ height: '100%', width: '100%' }}
        zoomControl={true}
      >
        <MapController center={currentPosition} />
        
        {/* OpenStreetMap Tiles */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Completed Route (Green Dotted Line) */}
        <Polyline
          positions={routeLine}
          color="green"
          weight={4}
          opacity={0.8}
          dashArray="10, 10"
        />

        {/* Remaining Route (Gray Dotted Line) */}
        <Polyline
          positions={remainingRoute}
          color="gray"
          weight={4}
          opacity={0.5}
          dashArray="10, 10"
        />

        {/* Origin Marker (Nagpur) */}
        <Marker position={nagpur}>
          <Popup>
            <div className="text-center p-2">
              <div className="text-2xl mb-2">📦</div>
              <strong className="text-lg">Origin: Nagpur</strong>
              <div className="text-sm text-gray-600 mt-1">Pickup Time: 10:30 AM</div>
              <div className="text-xs text-green-600 mt-1">✅ Departed</div>
            </div>
          </Popup>
        </Marker>

        {/* Destination Marker (Pune) */}
        <Marker position={pune}>
          <Popup>
            <div className="text-center p-2">
              <div className="text-2xl mb-2">🏠</div>
              <strong className="text-lg">Destination: Pune</strong>
              <div className="text-sm text-gray-600 mt-1">Expected: 6:30 PM</div>
              <div className="text-xs text-blue-600 mt-1">⏳ In Transit</div>
            </div>
          </Popup>
        </Marker>

        {/* Current Truck Location with Custom Emoji Icon */}
        <Marker position={currentPosition} icon={createTruckIcon()}>
          <Popup>
            <div className="text-center p-2">
              <div className="text-3xl mb-2">🚛</div>
              <strong className="text-lg">MH-31 Truck</strong>
              <div className="text-sm text-gray-600 mt-2">
                <div>📍 Location: <strong>{truckLocation.city}</strong></div>
                <div>📊 Progress: <strong>{truckLocation.progress}%</strong></div>
                <div>👨‍✈️ Driver: <strong>Raj Kumar</strong></div>
                <div>⚡ Speed: <strong>65 km/h</strong></div>
                <div className="mt-2 text-xs text-green-600">🟢 On Schedule</div>
              </div>
            </div>
          </Popup>
        </Marker>
      </MapContainer>

      {/* Custom CSS for truck icon */}
      <style jsx>{`
        .custom-truck-icon {
          background: transparent !important;
          border: none !important;
        }
      `}</style>
    </div>
  );
};

export default MapComponentDynamic;
