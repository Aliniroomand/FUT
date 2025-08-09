import { Outlet } from "react-router-dom";
import MainNavbar from "../components/MainNavbar";

const MainLayout = () => {
  return (
    <div className=" h-svh overflow-y-hidden  ">
      <div className=" top-0 h-1/12">
      <MainNavbar />
      </div>
      <main className=" top-1/12 h-9/12  ">
        <Outlet />
      </main>
        <footer className=" fixed bottom-0 h-fit z-50 w-full">
          <p className="z-50 bg-amber-200/70 text-black  text-sm">
            تمامی حقوق این سایت متعلق به اوس پوری می باشد و  هرگونه کپی یا
            استفاده از محتوا بدون ذکر منبع پیگرد قانونی دارد
          </p>
          <p className="bg-white/70 text-xs text-black">develope & desing by MP_Tech</p>
        </footer>
    </div>
  );
};

export default MainLayout;
