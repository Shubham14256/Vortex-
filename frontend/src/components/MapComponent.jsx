import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet';
import L from 'leaflet';
import { getTruckLocation } from '../services/api';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom truck icon
const truckIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const MapComponent = () => {
  const [truckLocation, setTruckLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Route coordinates
  const nagpur = [21.1458, 79.0882];
  const pune = [18.5204, 73.8567];

  // Fetch truck location
  const fetchTruckLocation = async () => {
    try {
      const data = await getTruckLocation();
      if (data.success) {
        setTruckLocation(data.location);
        setLastUpdate(new Date());
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching truck location:', error);
      setLoading(false);
    }
  };

  // Poll truck location every 2 seconds
  useEffect(() => {
    fetchTruckLocation();
    const interval = setInterval(fetchTruckLocation, 2000);
    return () => clearInterval(interval);
  }, []);

  if (loading || !truckLocation) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-100 rounded-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading map...</p>
        </div>
      </div>
    );
  }

  const currentPosition = [truckLocation.lat, truckLocation.lon];
  const routeLine = [nagpur, currentPosition, pune];

  return (
    <div className="h-full w-full rounded-lg overflow-hidden shadow-lg relative">
      {/* Live Indicator */}
      <div className="absolute top-4 right-4 z-[1000] bg-white px-3 py-2 rounded-lg shadow-lg flex items-center gap-2">
        <div className="relative">
          <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
          <div className="absolute inset-0 w-3 h-3 bg-red-500 rounded-full animate-ping"></div>
        </div>
        <span className="text-sm font-semibold text-gray-700">LIVE</span>
        <span className="text-xs text-gray-500">
          {lastUpdate.toLocaleTimeString()}
        </span>
      </div>
      
      <MapContainer
        center={[20.0, 76.0]}
        zoom={7}
        style={{ height: '100%', width: '100%' }}
      >
        {/* OpenStreetMap Tiles */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Route Line */}
        <Polyline
          positions={routeLine}
          color="red"
          weight={4}
          opacity={0.8}
        />

        {/* Origin Marker (Nagpur) */}
        <Marker position={nagpur}>
          <Popup>
            <div className="text-center">
              <strong>📦 Origin: Nagpur</strong>
              <br />
              Pickup Time: 10:30 AM
            </div>
          </Popup>
        </Marker>

        {/* Destination Marker (Pune) */}
        <Marker position={pune}>
          <Popup>
            <div className="text-center">
              <strong>🏠 Destination: Pune</strong>
              <br />
              Expected: 6:30 PM
            </div>
          </Popup>
        </Marker>

        {/* Current Truck Location */}
        <Marker position={currentPosition} icon={truckIcon}>
          <Popup>
            <div className="text-center">
              <strong>🚛 MH-31 Truck</strong>
              <br />
              Location: {truckLocation.city}
              <br />
              Progress: {truckLocation.progress}%
              <br />
              Driver: Raj Kumar
              <br />
              Speed: 65 km/h
            </div>
          </Popup>
        </Marker>

        {/* Checkpoints */}
        <CircleMarker
          center={[20.7, 78.1]}
          radius={8}
          fillColor="green"
          color="green"
          fillOpacity={0.7}
        >
          <Popup>✅ Checkpoint 1: Wardha (Completed)</Popup>
        </CircleMarker>

        <CircleMarker
          center={[19.8, 75.3]}
          radius={8}
          fillColor="orange"
          color="orange"
          fillOpacity={0.7}
        >
          <Popup>🔄 Checkpoint 2: Ahmednagar (In Transit)</Popup>
        </CircleMarker>

        <CircleMarker
          center={[19.2, 74.2]}
          radius={8}
          fillColor="gray"
          color="gray"
          fillOpacity={0.7}
        >
          <Popup>⏳ Checkpoint 3: Pune Outskirts (Pending)</Popup>
        </CircleMarker>
      </MapContainer>
    </div>
  );
};

export default MapComponent;