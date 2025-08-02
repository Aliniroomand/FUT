import { Link } from "react-router-dom";


const AnimatedCoin = ({ text, to, delay }) => (
  <Link
    to={to}
    className="w-20 h-20 bg-yellow-500 rounded-full flex items-center justify-center text-sm font-semibold text-black shadow-md hover:scale-110 transition-transform"
    style={{
      animation: `floatIn 1s ${delay} ease-out both`,
    }}
  >
    {text}
  </Link>
);
export default AnimatedCoin



