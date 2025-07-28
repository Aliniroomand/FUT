import { createBrowserRouter, Navigate, Outlet } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';

// pages
import HomePage from '@/pages/homePage';
import AdminLogin from '@/pages/AdminLogin';
import NotFoundPage from '@/pages/NotFoundPage';
// admin pages and layout
import AdminLayout from '@/pages/admin/Layout';
import Dashboard from '@/pages/admin/Dashboard';
import RangeManagement from '@/pages/admin/RangeManagement/RangeManagement';
import PlayerManagement from '@/pages/admin/RangeManagement/PlayerManagement';
import MethodManagement from '@/pages/admin/RangeManagement/MethodManagement';
import PriceManager from '../components/admin/PriceManager';

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,  // صفحه اصلی
  },
  {
    path: '/login',
    element: <AdminLogin />, // صفحه ورود ادمین
  },
  {
    path: '/admin',
    element: (
      <ProtectedRoute>
        <AdminLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <Navigate to="dashboard" replace /> },
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'mainPrices', element: <PriceManager /> },
      {
        path: 'rangeManagement',
        element: <Outlet />,
        children: [
          { path: 'player', element: <PlayerManagement /> },
          { path: 'range', element: <RangeManagement /> },
          { path: 'method', element: <MethodManagement /> },
        ],
      },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
]);

export default router;