import React from 'react';
import PriceManager from '../components/PriceManager';
import TransferMethods from '../components/transferMethod';

const AdminDashboard = () => {
  return (
    <div className="min-h-screen bg-black text-white p-8">
      <h1 className="text-2xl font-bold mb-6 text-[#B8860B]">پنل ادمین</h1>
      <PriceManager />
      <TransferMethods />
    </div>
  );
};

export default AdminDashboard;
