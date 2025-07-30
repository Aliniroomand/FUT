import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";
import { AdminRoute, UserRoute } from './ProtectedRoute';

// pages
import HomePage from "@/pages/homePage";
import AdminLogin from "@/pages/login/AdminLogin";
import NotFoundPage from "@/pages/NotFoundPage";
// admin pages and layout
import AdminLayout from "@/pages/admin/Layout";
import Dashboard from "@/pages/admin/Dashboard";
import RangeManagement from "@/pages/admin/RangeManagement/RangeManagement";
import PlayerManagement from "@/pages/admin/RangeManagement/PlayerManagement";
import MethodManagement from "@/pages/admin/RangeManagement/MethodManagement";
import PriceManager from "../components/admin/PriceManager";
import Register from "../pages/login/register";
// user profile
import UserProfile from "../pages/User/UserProfile";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />, // صفحه اصلی
  },
  {
    path: "/login",
    element: <AdminLogin />,
  },
  {
    path: "/register",
    element: <Register />,
  },

  {
    path: "/profile",
    element: (
      <UserRoute>
        <UserProfile />
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
