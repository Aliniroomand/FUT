import PriceManager from "../../components/admin/PriceManager";
import MakeAdmin from "../../components/admin/MakeAdmin";
import AdminEAAccountPanel from "../../components/admin/EAAcountsManagement/AdminEAAccountPanel";
import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import Show_live_price from "@/components/Show_live_price"


const Dashboard = () => {
  const makeAdminRef = useRef(null);
  const location = useLocation();

  return (
    <div className="container mx-auto px-2 md:px-8 py-4">
      <h1 className="text-2xl font-bold text-amber-500 mb-4">داشبورد ادمین</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <PriceManager/>
          <MakeAdmin/>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
