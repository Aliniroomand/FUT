import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";
import { AdminRoute, UserRoute } from "./ProtectedRoute";

// عمومی
import NotFoundPage from "@/pages/NotFoundPage";
import MainLayout from "@/pages/MainLayout";
import HomePage from "@/pages/home/homePage";
import Login from "@/pages/login/Login";
import Register from "@/pages/login/Register";
import ForgotPassword from "@/pages/login/ForgotPassword";
import ResetPassword from "@/pages/login/ResetPassword";


// کاربر
import UserLayout from "@/pages/User/UserLayout";
import UserDashboard from "@/pages/User/UserDashboard";
import UserTransactions from "@/pages/User/UserTransactions";

// ادمین
import AdminLayout from "@/pages/admin/Layout";
import Dashboard from "@/pages/admin/Dashboard";
import PriceManager from "@/components/admin/PriceManager";
import MakeAdminPage from "@/pages/admin/MakeAdminPage";
import PlayerManagement from "@/pages/admin/RangeManagement/PlayerManagement";
import RangeManagement from "@/pages/admin/RangeManagement/RangeManagement";
import MethodManagement from "@/pages/admin/RangeManagement/MethodManagement";
import TransactionsPage from "@/pages/TransactionsPage";
import AdminEAAccountPanel from "@/components/admin/EAAcountsManagement/AdminEAAccountPanel";
import TransactionsControl from "@/components/admin/TransactionsControl"
import AlertsPage from "../components/admin/Alerts/AlertsPage";
import ComingSoon from "../pages/ComingSoon";

const router = createBrowserRouter([
  // مسیرهای احراز هویت
  { path: "/login", element: <Login /> },
  { path: "/register", element: <Register /> },
  { path: "/forgot-password", element: <ForgotPassword /> },
  { path: "/reset-password", element: <ResetPassword /> },

  // مسیر اصلی با layout مشترک و navbar
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      // { path: "contact", element: <ComingSoon /> },
      // { path: "support", element: <ComingSoon /> },
      { path: "faq", element: <ComingSoon /> },
      // { path: "bot", element: <ComingSoon /> },
    ],
  },

  // مسیرهای کاربر
  {
    path: "/user",
    element: (
      <UserRoute>
        <UserLayout />
      </UserRoute>
    ),
    children: [
      { index: true, element: <Navigate to="dashboard" /> },
      { path: "dashboard", element: <UserDashboard /> },
      { path: "transactions", element: <UserTransactions /> },
    ],
  },

  // مسیرهای ادمین
  {
    path: "/admin",
    element: (
      <AdminRoute>
        <AdminLayout />
      </AdminRoute>
    ),
    children: [
      { index: true, element: <Navigate to="dashboard" /> },
      { path: "dashboard", element: <Dashboard /> },
      { path: "mainPrices", element: <PriceManager /> },
      { path: "make-admin", element: <MakeAdminPage /> },
      { path: "transactions", element: <TransactionsPage /> },
      { path: "ea-accounts", element:<AdminEAAccountPanel/>} ,
      { path: "transaction-control", element:<TransactionsControl/>} ,
      { path: "alerts", element:<AlertsPage/>} ,
      {
        path: "rangeManagement",
        element: <Outlet />,
        children: [
          { index: true, element: <Navigate to="player" /> },
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
