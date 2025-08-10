import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";

const StatusIcon = ({ status }) => {
  if (status === 1) {
    return <FaCheckCircle className=" text-green-500 ml-2" title="موفق" />;
  }
  return <FaTimesCircle className="  text-red-500 ml-2" title="ناموفق" />;
};

export default StatusIcon;
