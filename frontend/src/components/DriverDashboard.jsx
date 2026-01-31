import React, { useState, useEffect } from 'react';
import { Search, AlertTriangle, Wrench, DollarSign, RefreshCw, Gauge, Upload } from 'lucide-react';
import toast from 'react-hot-toast';
import { findLoad, checkSafety, diagnoseEngine, validateExpense, getSensors, refreshSensors } from '../services/api';
import WeatherWidget from './WeatherWidget';

const DriverDashboard = () => {
  const [loadingStates, setLoadingStates] = useState({
    findLoad: false,
    safety: false,
    engine: false,
    expense: false,
    sensors: false
  });
  const [result, setResult] = useState(null);
  const [sensors, setSensors] = useState(null);
  const [location, setLocation] = useState('Bangalore');
  const [expenseAmount, setExpenseAmount] = useState(1500);
  const [expenseItem, setExpenseItem] = useState('Fuel');
  const [uploadingFile, setUploadingFile] = useState(null);

  // Fetch sensors on mount
  useEffect(() => {
    fetchSensors();
  }, []);

  const fetchSensors = async () => {
    try {
      const data = await getSensors();
      if (data.success) {
        setSensors(data.sensors);
      }
    } catch (error) {
      console.error('Error fetching sensors:', error);
    }
  };

  const handleRefreshSensors = async () => {
    setLoadingStates(prev => ({ ...prev, sensors: true }));
    const toastId = toast.loading('🔄 Refreshing sensor data...');
    
    try {
      const data = await refreshSensors();
      if (data.success) {
        setSensors(data.sensors);
        toast.success('✅ Sensors refreshed successfully!', { id: toastId });
      }
    } catch (error) {
      console.error('Error refreshing sensors:', error);
      toast.error('❌ Failed to refresh sensors', { id: toastId });
    } finally {
      setLoadingStates(prev => ({ ...prev, sensors: false }));
    }
  };

  const handleFindLoad = async () => {
    setLoadingStates(prev => ({ ...prev, findLoad: true }));
    const toastId = toast.loading(`🔍 Searching for loads near ${location}...`);
    
    try {
      const data = await findLoad(location);
      setResult({ type: 'success', message: data.data });
      toast.success('✅ Found available loads!', { id: toastId });
    } catch (error) {
      setResult({ type: 'error', message: 'Failed to find load' });
      toast.error('❌ Failed to find loads', { id: toastId });
    } finally {
      setLoadingStates(prev => ({ ...prev, findLoad: false }));
    }
  };

  const handleSafetyCheck = async () => {
    setLoadingStates(prev => ({ ...prev, safety: true }));
    setUploadingFile('selfie');
    const toastId = toast.loading('📸 Uploading selfie...');
    
    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    toast.loading('🤖 AI analyzing drowsiness...', { id: toastId });
    
    try {
      const data = await checkSafety('driver_selfie.jpg');
      setResult({ type: 'success', message: data.data });
      toast.success('✅ Safety check complete!', { id: toastId });
    } catch (error) {
      setResult({ type: 'error', message: 'Safety check failed' });
      toast.error('❌ Safety check failed', { id: toastId });
    } finally {
      setLoadingStates(prev => ({ ...prev, safety: false }));
      setUploadingFile(null);
    }
  };

  const handleEngineCheck = async () => {
    setLoadingStates(prev => ({ ...prev, engine: true }));
    setUploadingFile('audio');
    const toastId = toast.loading('🎤 Uploading engine audio...');
    
    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    toast.loading('🔧 AI analyzing engine sounds...', { id: toastId });
    
    try {
      const data = await diagnoseEngine('engine_audio.mp3');
      setResult({ type: 'success', message: data.data });
      toast.success('✅ Engine diagnosis complete!', { id: toastId });
    } catch (error) {
      setResult({ type: 'error', message: 'Engine diagnosis failed' });
      toast.error('❌ Engine diagnosis failed', { id: toastId });
    } finally {
      setLoadingStates(prev => ({ ...prev, engine: false }));
      setUploadingFile(null);
    }
  };

  const handleExpenseValidation = async () => {
    setLoadingStates(prev => ({ ...prev, expense: true }));
    const toastId = toast.loading(`💰 Validating ₹${expenseAmount} for ${expenseItem}...`);
    
    try {
      const data = await validateExpense(expenseAmount, expenseItem, 'Fuel');
      setResult({ type: 'success', message: data.data });
      toast.success('✅ Expense validated!', { id: toastId });
    } catch (error) {
      setResult({ type: 'error', message: 'Expense validation failed' });
      toast.error('❌ Validation failed', { id: toastId });
    } finally {
      setLoadingStates(prev => ({ ...prev, expense: false }));
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-3xl font-bold text-gray-800">👨‍✈️ Driver Dashboard</h2>

      {/* Weather Widget */}
      <WeatherWidget lat={21.14} lon={79.08} city="Nagpur" />

      {/* IoT Sensors */}
      {sensors && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold flex items-center gap-2">
              <Gauge className="w-6 h-6 text-blue-600" />
              Live Engine Sensors
            </h3>
            <button
              onClick={handleRefreshSensors}
              disabled={loadingStates.sensors}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              <RefreshCw className={`w-4 h-4 ${loadingStates.sensors ? 'animate-spin' : ''}`} />
              {loadingStates.sensors ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">🌡️ Engine Temp</div>
              <div className="text-2xl font-bold text-gray-800">{sensors.engine_temp}°C</div>
              <div className={`text-xs ${sensors.engine_temp < 85 ? 'text-green-600' : 'text-yellow-600'}`}>
                {sensors.engine_temp < 85 ? '🟢 Normal' : '🟡 Warm'}
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">⚡ Battery</div>
              <div className="text-2xl font-bold text-gray-800">{sensors.battery_voltage}V</div>
              <div className={`text-xs ${sensors.battery_voltage > 13.8 ? 'text-green-600' : 'text-yellow-600'}`}>
                {sensors.battery_voltage > 13.8 ? '🟢 Good' : '🟡 Low'}
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">🛢️ Oil Pressure</div>
              <div className="text-2xl font-bold text-gray-800">{sensors.oil_pressure} PSI</div>
              <div className={`text-xs ${sensors.oil_pressure > 35 ? 'text-green-600' : 'text-red-600'}`}>
                {sensors.oil_pressure > 35 ? '🟢 Normal' : '🔴 Low'}
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">⚙️ RPM</div>
              <div className="text-2xl font-bold text-gray-800">{sensors.rpm}</div>
              <div className="text-xs text-green-600">🟢 Optimal</div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">⛽ Fuel Level</div>
              <div className="text-2xl font-bold text-gray-800">{sensors.fuel_level}%</div>
              <div className={`text-xs ${sensors.fuel_level > 25 ? 'text-green-600' : 'text-yellow-600'}`}>
                {sensors.fuel_level > 25 ? '🟢 Good' : '🟡 Low'}
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">❄️ Coolant</div>
              <div className="text-2xl font-bold text-gray-800">{sensors.coolant_temp}°C</div>
              <div className={`text-xs ${sensors.coolant_temp < 95 ? 'text-green-600' : 'text-yellow-600'}`}>
                {sensors.coolant_temp < 95 ? '🟢 Normal' : '🟡 Warm'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* AI Tools */}
      <div className="grid grid-cols-2 gap-6">
        {/* Find Return Load */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Search className="w-5 h-5 text-green-600" />
            Find Return Load
          </h3>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter location"
            className="w-full px-4 py-2 border rounded-lg mb-4"
          />
          <button
            onClick={handleFindLoad}
            disabled={loadingStates.findLoad}
            className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loadingStates.findLoad ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Searching...
              </>
            ) : (
              '🔍 Find Loads'
            )}
          </button>
        </div>

        {/* Safety Check */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            AI Safety Check
          </h3>
          <div className="mb-4">
            <label className="block text-sm text-gray-600 mb-2">
              Upload selfie for drowsiness detection
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-yellow-500 transition cursor-pointer">
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-500">
                {uploadingFile === 'selfie' ? 'Uploading...' : 'Click to upload or drag & drop'}
              </p>
            </div>
          </div>
          <button
            onClick={handleSafetyCheck}
            disabled={loadingStates.safety}
            className="w-full bg-yellow-600 text-white py-2 rounded-lg hover:bg-yellow-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loadingStates.safety ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                {uploadingFile === 'selfie' ? 'Uploading...' : 'Analyzing...'}
              </>
            ) : (
              '📸 Check Safety'
            )}
          </button>
        </div>

        {/* Engine Diagnosis */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Wrench className="w-5 h-5 text-blue-600" />
            Engine Diagnosis
          </h3>
          <div className="mb-4">
            <label className="block text-sm text-gray-600 mb-2">
              Upload engine audio for AI analysis
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-500 transition cursor-pointer">
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-500">
                {uploadingFile === 'audio' ? 'Uploading...' : 'Click to upload audio file'}
              </p>
            </div>
          </div>
          <button
            onClick={handleEngineCheck}
            disabled={loadingStates.engine}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loadingStates.engine ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                {uploadingFile === 'audio' ? 'Uploading...' : 'Diagnosing...'}
              </>
            ) : (
              '🔧 Diagnose Engine'
            )}
          </button>
        </div>

        {/* Expense Validation */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-purple-600" />
            Expense Validation
          </h3>
          <input
            type="number"
            value={expenseAmount}
            onChange={(e) => setExpenseAmount(Number(e.target.value))}
            placeholder="Amount"
            className="w-full px-4 py-2 border rounded-lg mb-2"
          />
          <input
            type="text"
            value={expenseItem}
            onChange={(e) => setExpenseItem(e.target.value)}
            placeholder="Item"
            className="w-full px-4 py-2 border rounded-lg mb-4"
          />
          <button
            onClick={handleExpenseValidation}
            disabled={loadingStates.expense}
            className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loadingStates.expense ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Validating...
              </>
            ) : (
              '💰 Validate Expense'
            )}
          </button>
        </div>
      </div>

      {/* Result Display */}
      {result && (
        <div className={`p-4 rounded-lg ${
          result.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        }`}>
          <h4 className="font-semibold mb-2">
            {result.type === 'success' ? '✅ Success' : '❌ Error'}
          </h4>
          <pre className="text-sm whitespace-pre-wrap">{result.message}</pre>
        </div>
      )}
    </div>
  );
};

export default DriverDashboard;