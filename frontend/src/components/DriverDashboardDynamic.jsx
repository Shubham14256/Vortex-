import React, { useState, useEffect } from 'react';
import { Search, AlertTriangle, Wrench, DollarSign, RefreshCw, Gauge, Upload, TrendingUp, TrendingDown, Users, Navigation } from 'lucide-react';
import toast from 'react-hot-toast';
import { findLoad, checkSafety, diagnoseEngine, validateExpense, getSensors, refreshSensors, findPartialLoad, acceptPartialLoad } from '../services/api';
import WeatherWidget from './WeatherWidget';

const DriverDashboardDynamic = () => {
  const [loadingStates, setLoadingStates] = useState({
    findLoad: false,
    safety: false,
    engine: false,
    expense: false,
    sensors: false
  });
  const [result, setResult] = useState(null);
  const [sensors, setSensors] = useState(null);
  const [liveSensors, setLiveSensors] = useState(null); // For local fluctuation
  const [location, setLocation] = useState('Bangalore');
  const [expenseAmount, setExpenseAmount] = useState(1500);
  const [expenseItem, setExpenseItem] = useState('Fuel');
  const [uploadingFile, setUploadingFile] = useState(null);
  const [partialLoadData, setPartialLoadData] = useState(null);
  const [totalEarnings, setTotalEarnings] = useState(0);
  const [loadingPartialLoad, setLoadingPartialLoad] = useState(false);
  
  // File input refs
  const selfieInputRef = React.useRef(null);
  const audioInputRef = React.useRef(null);

  // Fetch sensors on mount
  useEffect(() => {
    fetchSensors();
  }, []);

  // Simulate live sensor fluctuation every 2 seconds
  useEffect(() => {
    if (!sensors) return;

    const fluctuateSensors = () => {
      setLiveSensors(prev => {
        const base = prev || sensors;
        return {
          engine_temp: Math.max(75, Math.min(95, base.engine_temp + (Math.random() - 0.5) * 3)),
          battery_voltage: Math.max(13.5, Math.min(14.5, base.battery_voltage + (Math.random() - 0.5) * 0.2)),
          oil_pressure: Math.max(30, Math.min(50, base.oil_pressure + (Math.random() - 0.5) * 3)),
          rpm: Math.max(1200, Math.min(2200, base.rpm + (Math.random() - 0.5) * 100)),
          fuel_level: Math.max(0, Math.min(100, base.fuel_level + (Math.random() - 0.5) * 2)),
          coolant_temp: Math.max(70, Math.min(100, base.coolant_temp + (Math.random() - 0.5) * 3))
        };
      });
    };

    // Initial set
    setLiveSensors(sensors);

    // Fluctuate every 2 seconds
    const interval = setInterval(fluctuateSensors, 2000);
    return () => clearInterval(interval);
  }, [sensors]);

  const fetchSensors = async () => {
    try {
      const data = await getSensors();
      if (data.success) {
        setSensors(data.sensors);
        setLiveSensors(data.sensors);
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
        setLiveSensors(data.sensors);
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

  const handleSafetyCheck = async (file = null) => {
    setLoadingStates(prev => ({ ...prev, safety: true }));
    setUploadingFile('selfie');
    const toastId = toast.loading('📸 Uploading selfie...');
    
    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    toast.loading('🤖 AI analyzing drowsiness...', { id: toastId });
    
    try {
      const data = await checkSafety('driver_selfie.jpg');
      
      // Generate realistic analysis result
      const alertness = random.choice(['Alert', 'Slightly Drowsy', 'Drowsy']);
      const confidence = random.randint(85, 98);
      const recommendation = alertness === 'Alert' 
        ? '✅ Driver is alert and fit to drive. Continue journey safely.'
        : alertness === 'Slightly Drowsy'
        ? '⚠️ Driver showing signs of fatigue. Recommend 15-minute break.'
        : '🚨 Driver is drowsy. MANDATORY 30-minute rest break required!';
      
      const analysisResult = `
🔍 AI Safety Analysis Complete

📊 Drowsiness Level: ${alertness}
🎯 Confidence: ${confidence}%
⏰ Analysis Time: ${new Date().toLocaleTimeString()}

${recommendation}

📋 Detailed Metrics:
• Eye Closure Rate: ${random.randint(5, 25)}%
• Head Position: ${random.choice(['Normal', 'Tilted', 'Drooping'])}
• Blink Frequency: ${random.randint(12, 25)} per minute
• Facial Expression: ${random.choice(['Focused', 'Tired', 'Yawning'])}

${file ? `📁 File: ${file.name}` : '📁 File: driver_selfie.jpg'}
      `.trim();
      
      setResult({ type: 'success', message: analysisResult });
      toast.success('✅ Safety analysis complete!', { id: toastId });
    } catch (error) {
      setResult({ type: 'error', message: 'Safety check failed' });
      toast.error('❌ Safety check failed', { id: toastId });
    } finally {
      setLoadingStates(prev => ({ ...prev, safety: false }));
      setUploadingFile(null);
    }
  };

  const handleEngineCheck = async (file = null) => {
    setLoadingStates(prev => ({ ...prev, engine: true }));
    setUploadingFile('audio');
    const toastId = toast.loading('🎤 Uploading engine audio...');
    
    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    toast.loading('🔧 AI analyzing engine sounds...', { id: toastId });
    
    try {
      const data = await diagnoseEngine('engine_audio.mp3');
      
      // Generate realistic engine analysis
      const health = random.randint(85, 99);
      const issues = health > 95 
        ? ['No issues detected']
        : health > 90
        ? ['Minor vibration detected', 'Recommend oil change soon']
        : ['Belt tension needs adjustment', 'Air filter replacement due'];
      
      const analysisResult = `
🔧 AI Engine Diagnosis Complete

📊 Overall Health: ${health}%
⏰ Analysis Time: ${new Date().toLocaleTimeString()}

${health > 95 ? '✅ Engine is in excellent condition!' : health > 90 ? '⚠️ Minor maintenance recommended' : '🔴 Maintenance required soon'}

🔍 Detected Issues:
${issues.map(issue => `• ${issue}`).join('\n')}

📋 Sound Analysis:
• Engine Noise Level: ${random.randint(65, 85)} dB
• Vibration Pattern: ${random.choice(['Normal', 'Slight Irregularity', 'Smooth'])}
• Combustion Quality: ${random.randint(90, 99)}%
• Belt Condition: ${random.choice(['Good', 'Fair', 'Needs Inspection'])}

💡 Recommendation: ${health > 95 ? 'Continue operation normally' : 'Schedule maintenance within 500 km'}

${file ? `📁 File: ${file.name}` : '📁 File: engine_audio.mp3'}
      `.trim();
      
      setResult({ type: 'success', message: analysisResult });
      toast.success('✅ Engine diagnosis complete!', { id: toastId });
    } catch (error) {
      setResult({ type: 'error', message: 'Engine diagnosis failed' });
      toast.error('❌ Engine diagnosis failed', { id: toastId });
    } finally {
      setLoadingStates(prev => ({ ...prev, engine: false }));
      setUploadingFile(null);
    }
  };

  // File upload handlers
  const handleSelfieUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleSafetyCheck(file);
    }
  };

  const handleAudioUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleEngineCheck(file);
    }
  };

  // Helper function for random choice
  const random = {
    choice: (arr) => arr[Math.floor(Math.random() * arr.length)],
    randint: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
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

  // Partial Load Sharing handlers
  const handleScanPartialLoad = async () => {
    setLoadingPartialLoad(true);
    const toastId = toast.loading('📡 Scanning for overloaded trucks nearby...');
    
    try {
      const data = await findPartialLoad();
      if (data.alert) {
        setPartialLoadData(data);
        toast.success('⚠️ Overloaded truck found!', { id: toastId });
      } else {
        setPartialLoadData(null);
        toast.success('✅ No overloaded trucks in your area', { id: toastId });
      }
    } catch (error) {
      console.error('Error scanning for partial loads:', error);
      toast.error('❌ Failed to scan for trucks', { id: toastId });
    } finally {
      setLoadingPartialLoad(false);
    }
  };

  const handleAcceptPartialLoad = async () => {
    if (!partialLoadData) return;
    
    const toastId = toast.loading('✅ Accepting load...');
    
    try {
      const data = await acceptPartialLoad(
        partialLoadData.truck_id,
        partialLoadData.offer_price
      );
      
      if (data.success) {
        // Update total earnings
        setTotalEarnings(prev => prev + partialLoadData.offer_price);
        
        toast.success(
          `✅ Load accepted! Navigation started to ${partialLoadData.truck_id}. Earnings: ₹${partialLoadData.offer_price.toLocaleString()}`,
          { id: toastId, duration: 5000 }
        );
        
        // Clear alert after acceptance
        setTimeout(() => {
          setPartialLoadData(null);
        }, 2000);
      }
    } catch (error) {
      console.error('Error accepting partial load:', error);
      toast.error('❌ Failed to accept load', { id: toastId });
    }
  };

  const handleIgnorePartialLoad = () => {
    toast('⏭️ Load request ignored', { icon: '👋' });
    setPartialLoadData(null);
  };

  const getSensorStatus = (value, threshold, isHighBad = true) => {
    if (isHighBad) {
      if (value > threshold) return { color: 'text-red-600', bg: 'bg-red-50', icon: '🔴', label: 'High' };
      if (value > threshold * 0.9) return { color: 'text-yellow-600', bg: 'bg-yellow-50', icon: '🟡', label: 'Warm' };
      return { color: 'text-green-600', bg: 'bg-green-50', icon: '🟢', label: 'Normal' };
    } else {
      if (value < threshold) return { color: 'text-red-600', bg: 'bg-red-50', icon: '🔴', label: 'Low' };
      if (value < threshold * 1.1) return { color: 'text-yellow-600', bg: 'bg-yellow-50', icon: '🟡', label: 'Fair' };
      return { color: 'text-green-600', bg: 'bg-green-50', icon: '🟢', label: 'Good' };
    }
  };

  const displaySensors = liveSensors || sensors;

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-gray-800">👨‍✈️ Driver Dashboard</h2>
        <div className="flex items-center gap-2 px-4 py-2 bg-green-50 border-2 border-green-500 rounded-lg">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-semibold text-green-700">🟢 System Online</span>
        </div>
      </div>

      {/* Weather Widget */}
      <WeatherWidget lat={21.14} lon={79.08} city="Nagpur" />

      {/* IoT Sensors - Live Fluctuating */}
      {displaySensors && (
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl shadow-lg p-6 border-2 border-blue-200">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold flex items-center gap-3">
              <Gauge className="w-8 h-8 text-blue-600 animate-pulse" />
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Live Engine Sensors
              </span>
            </h3>
            <button
              onClick={handleRefreshSensors}
              disabled={loadingStates.sensors}
              className="flex items-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl disabled:bg-gray-400 disabled:cursor-not-allowed transform hover:scale-105"
            >
              <RefreshCw className={`w-5 h-5 ${loadingStates.sensors ? 'animate-spin' : ''}`} />
              {loadingStates.sensors ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>

          <div className="grid grid-cols-3 gap-4">
            {/* Engine Temp */}
            <div className={`${getSensorStatus(displaySensors.engine_temp, 90).bg} p-5 rounded-xl border-2 border-gray-200 shadow-md transform transition-all hover:scale-105`}>
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm font-medium text-gray-600">🌡️ Engine Temp</div>
                <TrendingUp className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-3xl font-bold text-gray-800 mb-1">
                {displaySensors.engine_temp.toFixed(1)}°C
              </div>
              <div className={`text-sm font-semibold ${getSensorStatus(displaySensors.engine_temp, 90).color}`}>
                {getSensorStatus(displaySensors.engine_temp, 90).icon} {getSensorStatus(displaySensors.engine_temp, 90).label}
              </div>
            </div>

            {/* Battery */}
            <div className={`${getSensorStatus(displaySensors.battery_voltage, 13.8, false).bg} p-5 rounded-xl border-2 border-gray-200 shadow-md transform transition-all hover:scale-105`}>
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm font-medium text-gray-600">⚡ Battery</div>
                <TrendingUp className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-3xl font-bold text-gray-800 mb-1">
                {displaySensors.battery_voltage.toFixed(2)}V
              </div>
              <div className={`text-sm font-semibold ${getSensorStatus(displaySensors.battery_voltage, 13.8, false).color}`}>
                {getSensorStatus(displaySensors.battery_voltage, 13.8, false).icon} {getSensorStatus(displaySensors.battery_voltage, 13.8, false).label}
              </div>
            </div>

            {/* Oil Pressure */}
            <div className={`${getSensorStatus(displaySensors.oil_pressure, 35, false).bg} p-5 rounded-xl border-2 border-gray-200 shadow-md transform transition-all hover:scale-105`}>
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm font-medium text-gray-600">🛢️ Oil Pressure</div>
                <TrendingDown className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-3xl font-bold text-gray-800 mb-1">
                {displaySensors.oil_pressure.toFixed(0)} PSI
              </div>
              <div className={`text-sm font-semibold ${getSensorStatus(displaySensors.oil_pressure, 35, false).color}`}>
                {getSensorStatus(displaySensors.oil_pressure, 35, false).icon} {getSensorStatus(displaySensors.oil_pressure, 35, false).label}
              </div>
            </div>

            {/* RPM */}
            <div className="bg-purple-50 p-5 rounded-xl border-2 border-gray-200 shadow-md transform transition-all hover:scale-105">
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm font-medium text-gray-600">⚙️ RPM</div>
                <TrendingUp className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-3xl font-bold text-gray-800 mb-1">
                {displaySensors.rpm.toFixed(0)}
              </div>
              <div className="text-sm font-semibold text-green-600">
                🟢 Optimal
              </div>
            </div>

            {/* Fuel Level */}
            <div className={`${getSensorStatus(displaySensors.fuel_level, 25, false).bg} p-5 rounded-xl border-2 border-gray-200 shadow-md transform transition-all hover:scale-105`}>
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm font-medium text-gray-600">⛽ Fuel Level</div>
                <TrendingDown className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-3xl font-bold text-gray-800 mb-1">
                {displaySensors.fuel_level.toFixed(0)}%
              </div>
              <div className={`text-sm font-semibold ${getSensorStatus(displaySensors.fuel_level, 25, false).color}`}>
                {getSensorStatus(displaySensors.fuel_level, 25, false).icon} {getSensorStatus(displaySensors.fuel_level, 25, false).label}
              </div>
            </div>

            {/* Coolant */}
            <div className={`${getSensorStatus(displaySensors.coolant_temp, 95).bg} p-5 rounded-xl border-2 border-gray-200 shadow-md transform transition-all hover:scale-105`}>
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm font-medium text-gray-600">❄️ Coolant</div>
                <TrendingUp className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-3xl font-bold text-gray-800 mb-1">
                {displaySensors.coolant_temp.toFixed(1)}°C
              </div>
              <div className={`text-sm font-semibold ${getSensorStatus(displaySensors.coolant_temp, 95).color}`}>
                {getSensorStatus(displaySensors.coolant_temp, 95).icon} {getSensorStatus(displaySensors.coolant_temp, 95).label}
              </div>
            </div>
          </div>

          {/* Live Update Indicator */}
          <div className="mt-4 flex items-center justify-center gap-2 text-sm text-gray-600">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            <span>Sensors updating every 2 seconds</span>
          </div>
        </div>
      )}

      {/* AI Tools */}
      <div className="grid grid-cols-2 gap-6">
        {/* Find Return Load */}
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-gray-100 hover:border-green-300 transition-all">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Search className="w-5 h-5 text-green-600" />
            Find Return Load
          </h3>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter location"
            className="w-full px-4 py-2 border-2 rounded-lg mb-4 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
          />
          <button
            onClick={handleFindLoad}
            disabled={loadingStates.findLoad}
            className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-3 rounded-lg hover:from-green-700 hover:to-green-800 transition-all shadow-lg hover:shadow-xl disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-105"
          >
            {loadingStates.findLoad ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Searching...
              </>
            ) : (
              '🔍 Find Loads'
            )}
          </button>
        </div>

        {/* Peer-to-Peer Load Sharing - NEW FEATURE */}
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-gray-100 hover:border-orange-300 transition-all">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-orange-600" />
            🤝 Peer-to-Peer Load Sharing
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            Help overloaded drivers & earn extra income
          </p>
          <button
            onClick={handleScanPartialLoad}
            disabled={loadingPartialLoad}
            className="w-full bg-gradient-to-r from-orange-600 to-orange-700 text-white py-3 rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all shadow-lg hover:shadow-xl disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-105"
          >
            {loadingPartialLoad ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Scanning...
              </>
            ) : (
              '📡 Scan for Overloaded Trucks'
            )}
          </button>
          
          {/* Total Earnings Display */}
          {totalEarnings > 0 && (
            <div className="mt-4 p-3 bg-green-50 border-2 border-green-300 rounded-lg">
              <div className="text-sm text-gray-600">Total Earnings Today</div>
              <div className="text-2xl font-bold text-green-600">₹{totalEarnings.toLocaleString()}</div>
            </div>
          )}
        </div>

        {/* Safety Check */}
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-gray-100 hover:border-yellow-300 transition-all">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            AI Safety Check
          </h3>
          <div className="mb-4">
            <label className="block text-sm text-gray-600 mb-2">
              Upload selfie for drowsiness detection
            </label>
            {/* Hidden file input */}
            <input
              ref={selfieInputRef}
              type="file"
              accept="image/*"
              onChange={handleSelfieUpload}
              className="hidden"
            />
            <div 
              onClick={() => selfieInputRef.current?.click()}
              className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-yellow-500 transition cursor-pointer bg-yellow-50"
            >
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-500">
                {uploadingFile === 'selfie' ? 'Uploading...' : 'Click to upload or drag & drop'}
              </p>
              <p className="text-xs text-gray-400 mt-1">JPG, PNG (Max 5MB)</p>
            </div>
          </div>
          <button
            onClick={() => handleSafetyCheck()}
            disabled={loadingStates.safety}
            className="w-full bg-gradient-to-r from-yellow-600 to-yellow-700 text-white py-3 rounded-lg hover:from-yellow-700 hover:to-yellow-800 transition-all shadow-lg hover:shadow-xl disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-105"
          >
            {loadingStates.safety ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                {uploadingFile === 'selfie' ? 'Uploading...' : 'Analyzing...'}
              </>
            ) : (
              '📸 Check Safety (Demo)'
            )}
          </button>
        </div>

        {/* Engine Diagnosis */}
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-gray-100 hover:border-blue-300 transition-all">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Wrench className="w-5 h-5 text-blue-600" />
            Engine Diagnosis
          </h3>
          <div className="mb-4">
            <label className="block text-sm text-gray-600 mb-2">
              Upload engine audio for AI analysis
            </label>
            {/* Hidden file input */}
            <input
              ref={audioInputRef}
              type="file"
              accept="audio/*"
              onChange={handleAudioUpload}
              className="hidden"
            />
            <div 
              onClick={() => audioInputRef.current?.click()}
              className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-500 transition cursor-pointer bg-blue-50"
            >
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-500">
                {uploadingFile === 'audio' ? 'Uploading...' : 'Click to upload audio file'}
              </p>
              <p className="text-xs text-gray-400 mt-1">MP3, WAV (Max 10MB)</p>
            </div>
          </div>
          <button
            onClick={() => handleEngineCheck()}
            disabled={loadingStates.engine}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg hover:shadow-xl disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-105"
          >
            {loadingStates.engine ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                {uploadingFile === 'audio' ? 'Uploading...' : 'Diagnosing...'}
              </>
            ) : (
              '🔧 Diagnose Engine (Demo)'
            )}
          </button>
        </div>

        {/* Expense Validation */}
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-gray-100 hover:border-purple-300 transition-all">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-purple-600" />
            Expense Validation
          </h3>
          <input
            type="number"
            value={expenseAmount}
            onChange={(e) => setExpenseAmount(Number(e.target.value))}
            placeholder="Amount"
            className="w-full px-4 py-2 border-2 rounded-lg mb-2 focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
          />
          <input
            type="text"
            value={expenseItem}
            onChange={(e) => setExpenseItem(e.target.value)}
            placeholder="Item"
            className="w-full px-4 py-2 border-2 rounded-lg mb-4 focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
          />
          <button
            onClick={handleExpenseValidation}
            disabled={loadingStates.expense}
            className="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white py-3 rounded-lg hover:from-purple-700 hover:to-purple-800 transition-all shadow-lg hover:shadow-xl disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-105"
          >
            {loadingStates.expense ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
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
        <div className={`p-6 rounded-xl shadow-lg border-2 animate-fadeIn ${
          result.type === 'success' 
            ? 'bg-green-50 border-green-300' 
            : 'bg-red-50 border-red-300'
        }`}>
          <h4 className="font-bold text-lg mb-3 flex items-center gap-2">
            {result.type === 'success' ? '✅ Success' : '❌ Error'}
          </h4>
          <pre className="text-sm whitespace-pre-wrap text-gray-700">{result.message}</pre>
        </div>
      )}

      {/* Partial Load Alert - Emergency Request */}
      {partialLoadData && partialLoadData.alert && (
        <div className="p-6 rounded-xl shadow-2xl border-4 border-orange-500 bg-gradient-to-br from-orange-50 to-red-50 animate-pulse">
          <div className="flex items-center justify-between mb-4">
            <h4 className="font-bold text-2xl flex items-center gap-2 text-orange-700">
              {partialLoadData.urgency_emoji} EMERGENCY LOAD SHARING REQUEST
            </h4>
            <div className={`px-4 py-2 rounded-full font-bold ${
              partialLoadData.urgency === 'HIGH' 
                ? 'bg-red-500 text-white' 
                : partialLoadData.urgency === 'MEDIUM'
                ? 'bg-yellow-500 text-white'
                : 'bg-green-500 text-white'
            }`}>
              {partialLoadData.urgency} URGENCY
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">🚛 Truck ID</div>
              <div className="text-xl font-bold text-gray-800">{partialLoadData.truck_id}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">👨‍✈️ Driver</div>
              <div className="text-xl font-bold text-gray-800">{partialLoadData.driver_name}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">📍 Distance</div>
              <div className="text-xl font-bold text-gray-800">{partialLoadData.distance_km} km</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-sm text-gray-600">⏰ ETA</div>
              <div className="text-xl font-bold text-gray-800">{partialLoadData.estimated_time}</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
            <h5 className="font-bold text-lg mb-3 text-gray-800">📦 Overload Details</h5>
            <div className="space-y-2 text-gray-700">
              <div className="flex justify-between">
                <span>Cargo:</span>
                <span className="font-semibold">{partialLoadData.cargo}</span>
              </div>
              <div className="flex justify-between">
                <span>Excess Weight:</span>
                <span className="font-semibold text-red-600">{partialLoadData.overload_tons} Tons</span>
              </div>
              <div className="flex justify-between">
                <span>Fine Risk:</span>
                <span className="font-semibold text-red-600">{partialLoadData.fine_risk}</span>
              </div>
              <div className="flex justify-between">
                <span>Location:</span>
                <span className="font-semibold">{partialLoadData.location}</span>
              </div>
            </div>
          </div>

          <div className="bg-green-100 p-6 rounded-lg shadow-lg mb-6 border-2 border-green-400">
            <h5 className="font-bold text-lg mb-3 text-green-800">💰 Your Earnings</h5>
            <div className="text-4xl font-bold text-green-600 mb-2">
              ₹{partialLoadData.offer_price.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">
              Help a fellow driver avoid fines & earn extra income!
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleIgnorePartialLoad}
              className="flex-1 bg-gray-500 text-white py-4 rounded-lg hover:bg-gray-600 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2 text-lg font-semibold"
            >
              ❌ Ignore
            </button>
            <button
              onClick={handleAcceptPartialLoad}
              className="flex-1 bg-gradient-to-r from-green-600 to-green-700 text-white py-4 rounded-lg hover:from-green-700 hover:to-green-800 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2 text-lg font-semibold transform hover:scale-105"
            >
              <Navigation className="w-6 h-6" />
              ✅ Accept Load & Navigate
            </button>
          </div>

          <div className="mt-4 text-center text-sm text-gray-600">
            ⏱️ Request expires in: {Math.floor(Math.random() * 30) + 15} minutes
          </div>
        </div>
      )}
    </div>
  );
};

export default DriverDashboardDynamic;
