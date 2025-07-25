import TransferMethods from '../components/admin/transferMethod';
import PriceManager from '../components/admin/PriceManager';
import { CardRangeForm } from '../components/admin/CardRangeForm';

const AdminDashboard = () => {
  return (
    <div dir="rtl" className="min-h-screen bg-black text-white p-8 ">
      <h1 className="text-2xl font-bold mb-6 text-[#B8860B]">پنل ادمین</h1>
      {/* <PriceManager /> */}
      {/* <TransferMethods /> */}
      <CardRangeForm />
    </div>
  );
};

export default AdminDashboard;
