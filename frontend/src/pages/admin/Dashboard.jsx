import PriceManager from "../../components/admin/PriceManager";
import MakeAdmin from "../../components/admin/MakeAdmin";
import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import Show_live_price from "@/components/Show_live_price"

// src/pages/admin/Dashboard.jsx
const Dashboard = () => {
  const makeAdminRef = useRef(null);
  const location = useLocation();


  return (
    <div>
      <h1 className="text-2xl font-bold text-amber-500 mb-4">داشبورد ادمین</h1>
      <PriceManager/>
    </div>
  );
};

export default Dashboard;
