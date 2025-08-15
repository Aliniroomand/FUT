import React, { useState, useEffect } from "react";
import { getTransactions } from "@/services/transactions";
import TransactionDetailsPopup from "@/components/transactions/TransactionDetailsPopup";



const TransactionsPage = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState({});
  const [total, setTotal] = useState(0);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const itemsPerPage = 10;

  useEffect(() => {
    fetchTransactions();
  }, [currentPage, filters]);

  const fetchTransactions = async () => {
    setLoading(true);
    setError(null);
    try {
      // Remove empty filter fields before sending to API
      const activeFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v && v.trim() !== "")
      );
      const data = await getTransactions({ ...activeFilters, page: currentPage, limit: itemsPerPage });
      setTransactions(data.items || []);
      setTotal(data.total || 0);
    } catch (err) {
      console.error(err);
      setError(err.message || "خطا در دریافت تراکنش‌ها");
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
    setCurrentPage(1);
  };

  const handleNextPage = () => {
    if (currentPage * itemsPerPage < total) setCurrentPage((prev) => prev + 1);
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) setCurrentPage((prev) => prev - 1);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto text-amber-300">
      <h1 className="text-3xl font-extrabold mb-6 text-amber-400 drop-shadow-lg">گزارش تراکنش‌ها</h1>

      {/* Filters */}
      <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <input
          type="text"
          name="customer_email"
          value={filters.customer_email || ""}
          placeholder="فیلتر بر اساس ایمیل"
          className="p-3 rounded-lg border border-amber-600 bg-amber-900/20 text-amber-300 placeholder-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-400"
          onChange={handleFilterChange}
        />
        <input
          type="text"
          name="customer_phone"
          value={filters.customer_phone || ""}
          placeholder="فیلتر بر اساس تلفن"
          className="p-3 rounded-lg border border-amber-600 bg-amber-900/20 text-amber-300 placeholder-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-400"
          onChange={handleFilterChange}
        />
        <input
          type="text"
          name="transaction_type"
          value={filters.transaction_type || ""}
          placeholder="فیلتر بر اساس نوع"
          className="p-3 rounded-lg border border-amber-600 bg-amber-900/20 text-amber-300 placeholder-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-400"
          onChange={handleFilterChange}
        />
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg glass-dark border border-amber-700 shadow-lg">
        <table className="min-w-full text-amber-300">
          <thead>
            <tr className="bg-amber-700/40 text-amber-100 font-semibold">
              <th className="py-3 px-6 border-b border-amber-600">ایمیل</th>
              <th className="py-3 px-6 border-b border-amber-600">تلفن</th>
              <th className="py-3 px-6 border-b border-amber-600">مقدار</th>
              <th className="py-3 px-6 border-b border-amber-600">نوع</th>
              <th className="py-3 px-6 border-b border-amber-600">تاریخ</th>
              <th className="py-3 px-6 border-b border-amber-600">عملیات</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="6" className="text-center py-4">
                  Loading...
                </td>
              </tr>
            ) : error ? (
              <tr>
                <td colSpan="6" className="text-center text-red-500 py-4">
                  {error}
                </td>
              </tr>
            ) : transactions.length > 0 ? (
              transactions.map((t) => (
                <tr
                  key={t.id}
                  className="hover:bg-amber-900/30 cursor-pointer transition-colors duration-200"
                  onClick={() => setSelectedTransaction(t)}
                >
                  <td className="py-3 px-6 border-b border-amber-600">{t.customer_email}</td>
                  <td className="py-3 px-6 border-b border-amber-600">{t.customer_phone}</td>
                  <td className="py-3 px-6 border-b border-amber-600">{t.amount}</td>
                  <td className="py-3 px-6 border-b border-amber-600">{t.transaction_type}</td>
                  <td className="py-3 px-6 border-b border-amber-600">{new Date(t.timestamp).toLocaleString()}</td>
                  <td className="py-3 px-6 border-b border-amber-600">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedTransaction(t);
                      }}
                      className="px-3 py-1 rounded-full bg-amber-500 text-dark-hard font-semibold hover:bg-amber-600 transition-shadow shadow-md"
                    >
                      مشاهده جزئیات
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="text-center py-4 text-amber-500">
                  موردی مطابق با جستجو پیدا نشد
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-6">
        <button
          onClick={handlePreviousPage}
          disabled={currentPage === 1}
          className="px-5 py-2 rounded-lg bg-amber-500 text-dark-hard font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-amber-600 transition"
        >
          قبلی
        </button>
        <span className="text-amber-400 font-bold">
          صفحه {currentPage} از {Math.ceil(total / itemsPerPage)}
        </span>
        <button
          onClick={handleNextPage}
          disabled={currentPage * itemsPerPage >= total}
          className="px-5 py-2 rounded-lg bg-amber-500 text-dark-hard font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-amber-600 transition"
        >
          بعدی
        </button>
      </div>

      {/* Transaction Details Popup */}
      <TransactionDetailsPopup
        transaction={selectedTransaction}
        onClose={() => setSelectedTransaction(null)}
      />
    </div>
  );
};

export default TransactionsPage;
