
import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import UserSidebar from "./UserSidebar";
import { FaBars } from "react-icons/fa";
import MainLayout from "../MainLayout";

const UserLayout = () => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <MainLayout>
      <div className="flex flex-row-reverse min-h-screen bg-dark-soft text-white relative">
        <button
          className="md:hidden absolute top-4 right-4 z-40 cursor-pointer"
          onClick={() => setIsOpen(true)}
        >
          <FaBars size={24} />
        </button>
        <UserSidebar isOpen={isOpen} setIsOpen={setIsOpen} />
        <main className="flex-1 p-4 md:p-6 overflow-x-auto">
          <Outlet />
        </main>
      </div>
    </MainLayout>
  );
};

export default UserLayout;
