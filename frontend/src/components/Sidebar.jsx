import React from 'react';
import { Truck, Users, Package, Activity } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'driver', name: 'Driver', icon: Truck, emoji: '👨‍✈️' },
    { id: 'owner', name: 'Owner', icon: Users, emoji: '💼' },
    { id: 'customer', name: 'Customer', icon: Package, emoji: '📦' },
  ];

  return (
    <div className="w-64 bg-primary text-white h-screen flex flex-col shadow-xl z-50 relative">
      {/* Header */}
      <div className="p-6 border-b border-blue-800">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Truck className="w-8 h-8" />
          Route-Rakshak
        </h1>
        <p className="text-blue-200 text-sm mt-1">Logistics Super-App</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <div className="space-y-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-white text-primary shadow-lg'
                    : 'text-blue-100 hover:bg-blue-800'
                }`}
              >
                <span className="text-2xl">{tab.emoji}</span>
                <span className="font-medium">{tab.name}</span>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Quick Stats */}
      <div className="p-4 border-t border-blue-800">
        <h3 className="text-sm font-semibold text-blue-200 mb-3">📊 Quick Stats</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-blue-200">Active Vehicles</span>
            <span className="font-bold">24</span>
          </div>
          <div className="flex justify-between">
            <span className="text-blue-200">Today's Deliveries</span>
            <span className="font-bold">156</span>
          </div>
          <div className="flex justify-between">
            <span className="text-blue-200">Revenue Today</span>
            <span className="font-bold">₹45,230</span>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="p-4 bg-blue-900">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Activity className="w-5 h-5 text-green-400 animate-pulse" />
            <div className="absolute inset-0 w-5 h-5">
              <div className="w-full h-full bg-green-400 rounded-full animate-ping opacity-75"></div>
            </div>
          </div>
          <div>
            <div className="text-sm font-bold text-green-400">🟢 System Online</div>
            <div className="text-xs text-blue-200">All services operational</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;