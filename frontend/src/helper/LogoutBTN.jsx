import { logout } from "@/services/auth";
import { FiLogOut } from "react-icons/fi";
import { useNavigate } from "react-router-dom";

const LogoutBTN = () => {
  const navigate=useNavigate()
  const handleLogout = () => {
    logout();
    navigate("/login");
  };
  return (
    <button
      onClick={handleLogout}
      className=" flex flex-row-reverse justify-start gap-2 bg-red-500 w-full text-shadow-lg text-shadow-black hover:bg-amber-600 text-white font-bold py-2 px-4 rounded"
    >
      <FiLogOut className="text-shadow-lg text-shadow-black" size={20} />
      خروج از حساب
    </button>
  );
};
export default LogoutBTN;
