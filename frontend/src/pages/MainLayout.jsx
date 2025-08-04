import {  Outlet } from 'react-router-dom';
import MainNavbar from '../components/MainNavbar';



const MainLayout = () => {
  return (
    <div className="  ">
      <MainNavbar />
      <main className="">
        <Outlet />
      </main>
    </div>
  );
};

export default MainLayout;
