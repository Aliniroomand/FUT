import PriceManager from "../../components/admin/PriceManager";
import MakeAdmin from "../../components/admin/MakeAdmin";
import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";

// src/pages/admin/Dashboard.jsx
const Dashboard = () => {
  const makeAdminRef = useRef(null);
  const location = useLocation();

  useEffect(() => {
    if (location.hash === "#make-admin" && makeAdminRef.current) {
      makeAdminRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [location]);

  return (
    <div>
      <h1 className="text-2xl font-bold text-amber-500 mb-4">داشبورد ادمین</h1>
      <PriceManager/>
      <div ref={makeAdminRef} id="make-admin">
        <MakeAdmin/>
      </div>
    </div>
  );
};

export default Dashboard;
