import React, { useState, useEffect } from 'react';
import { Play, Square, RotateCcw, MapPin } from 'lucide-react';
import toast from 'react-hot-toast';
import MapComponentDynamic from './MapComponentDynamic';
import { getTruckLocation, moveTruck, resetTruck, toggleLiveTracking } from '../services/api';

const CustomerDashboard = () => {
  const [truckLocation, setTruckLocation] = useState(null);
  const [liveTracking, setLiveTracking] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    fetchLocation();
  }, []);

  const fetchLocation = async () => {
    try {
      const data = await getTruckLocation();
      if (data.success) {
        setTruckLocation(data.location);
        setLiveTracking(data.live_tracking);
      }
    } catch (error) {
      console.error('Error fetching location:', error);
    }
  };

  const handleMoveTruck = async () => {
    setActionLoading(true);
    const toastId = toast.loading('🚛 Moving truck to next checkpoint...');
    
    try {
      const data = await moveTruck();
      if (data.success) {
        setTruckLocation(data.location);
        toast.success(`✅ Truck moved to ${data.location.city}!`, { id: toastId });
      }
    } catch (error) {
      console.error('Error moving truck:', error);
      toast.error('❌ Failed to move truck', { id: toastId });
    } finally {
      setActionLoading(false);
    }
  };

  const handleResetTruck = async () => {
    setActionLoading(true);
    const toastId = toast.loading('🔄 Resetting journey to Nagpur...');
    
    try {
      const data = await resetTruck();
      if (data.success) {
        setTruckLocation(data.location);
        toast.success('✅ Journey reset to starting point!', { id: toastId });
      }
    } catch (error) {
      console.error('Error resetting truck:', error);
      toast.error('❌ Failed to reset journey', { id: toastId });
    } finally {
      setActionLoading(false);
    }
  };

  const handleToggleTracking = async () => {
    setActionLoading(true);
    const toastId = toast.loading(liveTracking ? '⏸️ Stopping live tracking...' : '▶️ Starting live tracking...');
    
    try {
      const data = await toggleLiveTracking();
      if (data.success) {
        setLiveTracking(data.live_tracking);
        if (data.live_tracking) {
          toast.success('✅ Live tracking started! Truck will move automatically.', { id: toastId });
        } else {
          toast.success('⏸️ Live tracking paused.', { id: toastId });
        }
      }
    } catch (error) {
      console.error('Error toggling tracking:', error);
      toast.error('❌ Failed to toggle tracking', { id: toastId });
    } finally {
      setActionLoading(false);
    }
  };

  const distance_covered = truckLocation ? Math.floor(346 * truckLocation.progress / 100) : 0;
  const remaining_distance = 346 - distance_covered;

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-3xl font-bold text-gray-800">📦 Customer Tracking Portal</h2>

      <div className="grid grid-cols-3 gap-6">
        {/* Map Section */}
        <div className="col-span-2 space-y-4">
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold">🗺️ Live Tracking Map</h3>
              <div className="flex gap-2">
                <button
                  onClick={handleToggleTracking}
                  disabled={actionLoading}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed ${
                    liveTracking
                      ? 'bg-red-600 text-white hover:bg-red-700'
                      : 'bg-green-600 text-white hover:bg-green-700'
                  }`}
                >
                  {liveTracking ? (
                    <>
                      <Square className="w-4 h-4" />
                      Stop Tracking
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4" />
                      Start Live Tracking
                    </>
                  )}
                </button>
                <button
                  onClick={handleMoveTruck}
                  disabled={actionLoading}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <MapPin className="w-4 h-4" />
                  Manual Step
                </button>
                <button
                  onClick={handleResetTruck}
                  disabled={actionLoading}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <RotateCcw className="w-4 h-4" />
                  Reset
                </button>
              </div>
            </div>
            <div className="h-[500px]">
              <MapComponentDynamic />
            </div>
          </div>

          {/* Live Tracking Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4">📊 Live Tracking Status</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600">Distance Covered</div>
                <div className="text-2xl font-bold text-gray-800">{distance_covered} km</div>
                <div className="text-xs text-green-600">{truckLocation?.progress}%</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600">Current Speed</div>
                <div className="text-2xl font-bold text-gray-800">
                  {truckLocation?.progress < 100 ? '65 km/h' : '0 km/h'}
                </div>
                <div className="text-xs text-blue-600">
                  {liveTracking ? '🔴 LIVE' : '⏸️ Paused'}
                </div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600">ETA</div>
                <div className="text-2xl font-bold text-gray-800">
                  {truckLocation?.progress < 100 ? `${(remaining_distance / 65).toFixed(1)}h` : '🏁 Arrived'}
                </div>
                <div className="text-xs text-green-600">⏰ On Time</div>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar Info */}
        <div className="space-y-4">
          {/* Package Details */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">📦 Package Details</h3>
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-gray-600">Tracking ID</div>
                <div className="font-semibold">RR-2024-001234</div>
              </div>
              <div>
                <div className="text-gray-600">Order Date</div>
                <div className="font-semibold">Jan 30, 2024</div>
              </div>
              <div>
                <div className="text-gray-600">Expected Delivery</div>
                <div className="font-semibold">Jan 31, 2024</div>
              </div>
              <div>
                <div className="text-gray-600">Package Weight</div>
                <div className="font-semibold">2.5 kg</div>
              </div>
            </div>
          </div>

          {/* Vehicle Details */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">🚛 Vehicle Details</h3>
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-gray-600">Vehicle</div>
                <div className="font-semibold">TN-01-AB-1234</div>
              </div>
              <div>
                <div className="text-gray-600">Driver</div>
                <div className="font-semibold">Raj Kumar</div>
              </div>
              <div>
                <div className="text-gray-600">Contact</div>
                <div className="font-semibold">+91 98765 43210</div>
              </div>
              <div>
                <div className="text-gray-600">Current Location</div>
                <div className="font-semibold">{truckLocation?.city || 'Loading...'}</div>
              </div>
            </div>
          </div>

          {/* Delivery Address */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">📍 Delivery Address</h3>
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-gray-600">Name</div>
                <div className="font-semibold">John Doe</div>
              </div>
              <div>
                <div className="text-gray-600">Address</div>
                <div className="font-semibold">123, MG Road</div>
              </div>
              <div>
                <div className="text-gray-600">City</div>
                <div className="font-semibold">Pune, MH</div>
              </div>
              <div>
                <div className="text-gray-600">PIN</div>
                <div className="font-semibold">411001</div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">📞 Quick Actions</h3>
            <div className="space-y-2">
              <button className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition">
                📞 Call Driver
              </button>
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                📧 Send Message
              </button>
              <button className="w-full px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition">
                📋 Delivery Instructions
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerDashboard;