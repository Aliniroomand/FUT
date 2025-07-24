// src/components/admin/AdminDashboard.jsx
import { useState } from 'react';
import PlayerManagement from "@/components/admin/PlayerManagement/PlayerManagement"
import RangeManagement from "@/components/admin/RangeManagement/RangeManagement";
import TransferMethod from "@/components/admin/TransferMethod";

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('players');

  const tabs = [
    { id: 'players', label: 'مدیریت بازیکنان' },
    { id: 'ranges', label: 'مدیریت بازه‌ها' },
    { id: 'methods', label: 'مدیریت روش‌های انتقال' }
  ];

  return (
    <div className="bg-gray-900 min-h-screen p-4 text-white">
      <h1 className="text-2xl font-bold mb-6 text-amber-500 border-b border-amber-500 pb-2">
        پنل مدیریت ادمین
      </h1>
      
      {/* تب‌های ناوبری */}
      <div className="flex border-b border-gray-700 mb-6">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 font-medium ${activeTab === tab.id 
              ? 'text-amber-400 border-b-2 border-amber-400' 
              : 'text-gray-400 hover:text-white'}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* محتوای تب‌ها */}
      <div className="bg-gray-800 rounded-lg p-4">
        {activeTab === 'players' && <PlayerManagement />}
        {activeTab === 'ranges' && <RangeManagement />}
        {activeTab === 'methods' && <TransferMethod />}
      </div>
    </div>
  );
};

export default AdminDashboard;