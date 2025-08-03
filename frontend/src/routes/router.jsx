import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";
import { AdminRoute, UserRoute } from './ProtectedRoute';

// pages
import HomePage from "@/pages/home/homePage";
import Login from "@/pages/login/Login";
import NotFoundPage from "@/pages/NotFoundPage";
// admin pages and layout
import AdminLayout from "@/pages/admin/Layout";
import Dashboard from "@/pages/admin/Dashboard";
import RangeManagement from "@/pages/admin/RangeManagement/RangeManagement";
import PlayerManagement from "@/pages/admin/RangeManagement/PlayerManagement";
import MethodManagement from "@/pages/admin/RangeManagement/MethodManagement";
import PriceManager from "../components/admin/PriceManager";
import MakeAdminPage from "@/pages/admin/MakeAdminPage";
// user profile
import UserProfile from "../pages/User/UserProfile";
import UserDashboard from "../pages/User/UserDashboard";
import Register from "../pages/login/register";
import ForgotPassword from "../pages/login/ForgotPassword";
import ResetPassword from "../pages/login/ResetPassword";


const router = createBrowserRouter([
  {
    path: "/forgot-password",
    element: <ForgotPassword />,
  },
  {
    path: "/reset-password",
    element: <ResetPassword />,
  },
  {
    path: "/",
    element: <HomePage />, 
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/register",
    element: <Register />,
  },

  {
    path: "/profile",
    element: (
      <UserRoute>
        <UserDashboard />
      </UserRoute>
    ),
  },

  {
    path: "/admin",
    element: (
      <AdminRoute>
        <AdminLayout />
      </AdminRoute>
    ),
    children: [
      { index: true, element: <Navigate to="dashboard" replace /> },
      { path: "dashboard", element: <Dashboard /> },
      { path: "mainPrices", element: <PriceManager /> },
      { path: "make-admin", element: <MakeAdminPage /> },
      {
        path: "rangeManagement",
        element: <Outlet />,
        children: [
          { path: "player", element: <PlayerManagement /> },
          { path: "range", element: <RangeManagement /> },
          { path: "method", element: <MethodManagement /> },
        ],
      },
    ],
  },
  { path: "*", element: <NotFoundPage /> },
]);

export default router;
