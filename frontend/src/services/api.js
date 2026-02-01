import axios from 'axios';

const API_BASE_URL = 'https://vortex-backend-usex.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// AI Agent Services
export const findLoad = async (location) => {
  const response = await api.post('/api/find-load', { location });
  return response.data;
};

export const checkSafety = async (imagePath, driverStatus = 'active') => {
  const response = await api.post('/api/check-safety', {
    image_path: imagePath,
    driver_status: driverStatus,
  });
  return response.data;
};

export const diagnoseEngine = async (audioPath, vehicleId = 'TN-01-AB-1234') => {
  const response = await api.post('/api/diagnose-engine', {
    audio_path: audioPath,
    vehicle_id: vehicleId,
  });
  return response.data;
};

export const validateExpense = async (amount, item, category = 'General') => {
  const response = await api.post('/api/validate-expense', {
    amount,
    item,
    category,
  });
  return response.data;
};

// Truck Location Services
export const getTruckLocation = async () => {
  const response = await api.get('/api/truck-location');
  return response.data;
};

export const moveTruck = async () => {
  const response = await api.post('/api/truck-location/move');
  return response.data;
};

export const resetTruck = async () => {
  const response = await api.post('/api/truck-location/reset');
  return response.data;
};

export const toggleLiveTracking = async () => {
  const response = await api.post('/api/truck-location/toggle-tracking');
  return response.data;
};

// Fleet Management Services
export const getFleet = async () => {
  const response = await api.get('/api/fleet');
  return response.data;
};

export const addVehicle = async (vehicle) => {
  const response = await api.post('/api/fleet/add', vehicle);
  return response.data;
};

// IoT Sensor Services
export const getSensors = async () => {
  const response = await api.get('/api/sensors');
  return response.data;
};

export const refreshSensors = async () => {
  const response = await api.post('/api/sensors/refresh');
  return response.data;
};

// Weather Service
export const getWeather = async (lat = 21.14, lon = 79.08, city = 'Nagpur') => {
  const response = await api.get('/api/weather', {
    params: { lat, lon, city },
  });
  return response.data;
};

// System Logs Service
export const getSystemLogs = async () => {
  const response = await api.get('/api/system-logs');
  return response.data;
};

// Partial Load Sharing Services
export const findPartialLoad = async () => {
  const response = await api.post('/api/find-partial-load');
  return response.data;
};

export const acceptPartialLoad = async (truckId, earnings) => {
  const response = await api.post('/api/accept-partial-load', {
    truck_id: truckId,
    earnings: earnings
  });
  return response.data;
};

export default api;
