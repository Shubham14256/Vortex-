import React, { useState } from 'react';
import { Truck, Users, Package } from 'lucide-react';
import { Toaster } from 'react-hot-toast';
import DriverDashboardDynamic from './components/DriverDashboardDynamic';
import OwnerDashboard from './components/OwnerDashboard';
import CustomerDashboard from './components/CustomerDashboard';
import Sidebar from './components/Sidebar';

function App() {
  const [activeTab, setActiveTab] = useState('driver');

  const tabs = [
    { id: 'driver', label: 'Driver', icon: Truck },
    { id: 'owner', label: 'Fleet Owner', icon: Users },
    { id: 'customer', label: 'Customer', icon: Package },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Toast Notifications */}
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            duration: 4000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header with Tabs */}
        <header className="bg-white shadow-sm">
          <div className="px-6 py-4">
            <h1 className="text-2xl font-bold text-gray-800 mb-4">
              🚛 Route-Rakshak Logistics Super-App
            </h1>
            <div className="flex gap-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition ${
                      activeTab === tab.id
                        ? 'bg-primary text-white shadow-md'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {tab.label}
                  </button>
                );
              })}
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto">
          {activeTab === 'driver' && <DriverDashboardDynamic />}
          {activeTab === 'owner' && <OwnerDashboard />}
          {activeTab === 'customer' && <CustomerDashboard />}
        </main>
      </div>
    </div>
  );
}

export default App;
