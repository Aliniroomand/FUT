import {  Outlet } from 'react-router-dom';
import MainNavbar from '../components/MainNavbar';



const MainLayout = () => {
  return (
    <div className="  ">
      <MainNavbar />
      <main className="pt-15">
        <Outlet />
      </main>
    </div>
  );
};

export default MainLayout;
