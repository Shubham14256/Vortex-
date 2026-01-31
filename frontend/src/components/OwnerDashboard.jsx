import React, { useState, useEffect } from 'react';
import { Truck, TrendingUp, AlertCircle, Plus, X } from 'lucide-react';
import toast from 'react-hot-toast';
import { getFleet, addVehicle } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const OwnerDashboard = () => {
  const [fleet, setFleet] = useState([]);
  const [loading, setLoading] = useState(true);
  const [addingVehicle, setAddingVehicle] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newVehicle, setNewVehicle] = useState({
    id: '',
    driver: '',
    route: '',
    status: 'Starting',
    eta: ''
  });

  // Financial data for charts
  const financialData = [
    { day: 'Mon', Income: 45000, Expense: 32000, Profit: 13000 },
    { day: 'Tue', Income: 52000, Expense: 38000, Profit: 14000 },
    { day: 'Wed', Income: 48000, Expense: 35000, Profit: 13000 },
    { day: 'Thu', Income: 61000, Expense: 42000, Profit: 19000 },
    { day: 'Fri', Income: 55000, Expense: 39000, Profit: 16000 },
    { day: 'Sat', Income: 67000, Expense: 48000, Profit: 19000 },
    { day: 'Sun', Income: 45230, Expense: 33000, Profit: 12230 },
  ];

  useEffect(() => {
    fetchFleet();
  }, []);

  const fetchFleet = async () => {
    try {
      const data = await getFleet();
      if (data.success) {
        setFleet(data.vehicles);
      }
    } catch (error) {
      console.error('Error fetching fleet:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddVehicle = async (e) => {
    e.preventDefault();
    setAddingVehicle(true);
    const toastId = toast.loading(`🚛 Adding vehicle ${newVehicle.id}...`);
    
    try {
      await addVehicle(newVehicle);
      toast.success(`✅ Vehicle ${newVehicle.id} added successfully!`, { id: toastId });
      setShowAddForm(false);
      setNewVehicle({ id: '', driver: '', route: '', status: 'Starting', eta: '' });
      
      // Refresh fleet data immediately
      await fetchFleet();
    } catch (error) {
      console.error('Error adding vehicle:', error);
      toast.error('❌ Failed to add vehicle', { id: toastId });
    } finally {
      setAddingVehicle(false);
    }
  };

  const getStatusColor = (status) => {
    if (status.includes('On Road')) return 'bg-green-100 text-green-800';
    if (status.includes('Starting')) return 'bg-blue-100 text-blue-800';
    if (status.includes('Completed')) return 'bg-gray-100 text-gray-800';
    return 'bg-yellow-100 text-yellow-800';
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-gray-800">💼 Fleet Owner Dashboard</h2>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 transition"
        >
          <Plus className="w-5 h-5" />
          Add Vehicle
        </button>
      </div>

      {/* Add Vehicle Form */}
      {showAddForm && (
        <div className="bg-white rounded-lg shadow-md p-6 border-2 border-blue-500">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Add New Vehicle</h3>
            <button
              onClick={() => setShowAddForm(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <form onSubmit={handleAddVehicle} className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Vehicle ID (e.g., TN-05-XY-1234)"
              value={newVehicle.id}
              onChange={(e) => setNewVehicle({ ...newVehicle, id: e.target.value })}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <input
              type="text"
              placeholder="Driver Name"
              value={newVehicle.driver}
              onChange={(e) => setNewVehicle({ ...newVehicle, driver: e.target.value })}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <input
              type="text"
              placeholder="Route (e.g., Chennai → Bangalore)"
              value={newVehicle.route}
              onChange={(e) => setNewVehicle({ ...newVehicle, route: e.target.value })}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <select
              value={newVehicle.status}
              onChange={(e) => setNewVehicle({ ...newVehicle, status: e.target.value })}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="Starting">Starting</option>
              <option value="On Road">On Road</option>
              <option value="Completed">Completed</option>
              <option value="Maintenance">Maintenance</option>
            </select>
            <input
              type="text"
              placeholder="ETA (e.g., 3h 30m)"
              value={newVehicle.eta}
              onChange={(e) => setNewVehicle({ ...newVehicle, eta: e.target.value })}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="submit"
              disabled={addingVehicle}
              className="col-span-2 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {addingVehicle ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Adding Vehicle...
                </>
              ) : (
                <>
                  <Plus className="w-4 h-4" />
                  Add Vehicle
                </>
              )}
            </button>
          </form>
        </div>
      )}

      {/* Fleet Metrics */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Vehicles</p>
              <p className="text-3xl font-bold text-gray-800">{fleet.length}</p>
            </div>
            <Truck className="w-12 h-12 text-blue-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Active Trips</p>
              <p className="text-3xl font-bold text-gray-800">
                {fleet.filter(v => v.status.includes('On Road')).length}
              </p>
            </div>
            <TrendingUp className="w-12 h-12 text-green-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Available</p>
              <p className="text-3xl font-bold text-gray-800">
                {fleet.filter(v => v.status.includes('Starting')).length}
              </p>
            </div>
            <AlertCircle className="w-12 h-12 text-yellow-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Completed</p>
              <p className="text-3xl font-bold text-gray-800">
                {fleet.filter(v => v.status.includes('Completed')).length}
              </p>
            </div>
            <Truck className="w-12 h-12 text-gray-600 opacity-20" />
          </div>
        </div>
      </div>

      {/* Financial Chart */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4">📊 Weekly Income vs Expense Analysis</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={financialData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Income" fill="#10b981" />
            <Bar dataKey="Expense" fill="#ef4444" />
            <Bar dataKey="Profit" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Fleet Table */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4">🚛 Fleet Overview</h3>
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Vehicle ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Driver
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Route
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ETA
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {fleet.map((vehicle, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {vehicle.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {vehicle.driver}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {vehicle.route}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(vehicle.status)}`}>
                        {vehicle.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {vehicle.eta}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default OwnerDashboard;