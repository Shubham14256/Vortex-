import React, { useEffect, useState } from 'react';
import { Cloud, Wind, RefreshCw } from 'lucide-react';
import { getWeather } from '../services/api';

const WeatherWidget = ({ lat, lon, city }) => {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchWeather = async () => {
    setLoading(true);
    try {
      const data = await getWeather(lat, lon, city);
      if (data.success) {
        setWeather(data.weather);
      }
    } catch (error) {
      console.error('Error fetching weather:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeather();
  }, [lat, lon, city]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!weather) return null;

  return (
    <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg shadow-md p-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <Cloud className="w-5 h-5" />
          Live Weather
        </h3>
        <button
          onClick={fetchWeather}
          className="p-1 hover:bg-blue-200 rounded-full transition"
          title="Refresh weather"
        >
          <RefreshCw className="w-4 h-4 text-gray-600" />
        </button>
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-gray-600">📍 {weather.city}</span>
          <span className={`text-xs px-2 py-1 rounded ${
            weather.success ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800'
          }`}>
            {weather.status}
          </span>
        </div>

        <div className="flex items-center gap-4 text-2xl font-bold text-gray-800">
          <span className="text-4xl">{weather.emoji}</span>
          <span>{weather.temperature}°C</span>
        </div>

        <div className="flex items-center gap-2 text-gray-600">
          <Wind className="w-4 h-4" />
          <span>Wind: {weather.windspeed} km/h</span>
        </div>
      </div>
    </div>
  );
};

export default WeatherWidget;