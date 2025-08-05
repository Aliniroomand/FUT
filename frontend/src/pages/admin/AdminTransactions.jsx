import  { useEffect, useState } from "react";
import { getTransactions } from "@/services/transactions";
import TransactionTable from "@/components/transactions/TransactionTable";
import Pagination from "@/components/common/Pagination";
import Tesst from "@/components/Tesst"
const AdminTransactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(20);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await getTransactions(page, limit);
        setTransactions(data.items);
        setTotal(data.total);
      } catch (err) {
        setTransactions([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [page, limit]);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">گزارش تراکنش‌ها</h2>
      <Tesst/>
      {loading ? (
        <div>در حال بارگذاری...</div>
      ) : (
        <>
          <TransactionTable transactions={transactions} />
          <Pagination
            page={page}
            limit={limit}
            total={total}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
};

export default AdminTransactions;
