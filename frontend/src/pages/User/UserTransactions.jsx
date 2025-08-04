import React, { useEffect, useState } from "react";
import axios from "axios";

const UserTransactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(20);

  useEffect(() => {
    const fetchTransactions = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem("access_token");
        const res = await axios.get(`/api/transactions?skip=${(page - 1) * limit}&limit=${limit}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setTransactions(res.data.items);
        setTotal(res.data.total);
      } catch (err) {
        setTransactions([]);
      } finally {
        setLoading(false);
      }
    };
    fetchTransactions();
  }, [page, limit]);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">تراکنش‌های من</h2>
      {loading ? (
        <div>در حال بارگذاری...</div>
      ) : (
        <>
          <table className="w-full text-sm border">
            <thead>
              <tr>
                <th>شناسه</th>
                <th>نام کارت</th>
                <th>قیمت خرید</th>
                <th>قیمت فروش</th>
                <th>مبلغ کل</th>
                <th>وضعیت</th>
                <th>تسویه</th>
                <th>نوع بدهی/طلب</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((t) => (
                <tr key={t.id}>
                  <td>{t.id}</td>
                  <td>{t.card_name || '-'}</td>
                  <td>{t.buy_price || '-'}</td>
                  <td>{t.sell_price || '-'}</td>
                  <td>{t.amount}</td>
                  <td>{t.is_successful ? 'موفق' : 'ناموفق'}</td>
                  <td>{t.is_settled ? 'تسویه شده' : 'تسویه نشده'}</td>
                  <td style={{color: t.debt_or_credit_type === 'debt' ? 'red' : 'green'}}>
                    {t.debt_or_credit || '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="flex justify-between items-center mt-4">
            <button disabled={page === 1} onClick={() => setPage(page - 1)} className="btn">قبلی</button>
            <span>
              صفحه {page} از {Math.ceil(total / limit)}
            </span>
            <button disabled={page * limit >= total} onClick={() => setPage(page + 1)} className="btn">بعدی</button>
          </div>
        </>
      )}
    </div>
  );
};

export default UserTransactions;
