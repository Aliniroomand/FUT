// src/components/transactions/TransactionTable.jsx
const TransactionTable = ({ transactions }) => {
  return (
    <table className="w-full text-sm border glass-dark">
      <thead className="border-b-2 p-10 glass-dark">
        <tr>
          <th>شناسه</th>
          <th>نام مشتری</th>
          <th>شماره مشتری</th>
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
        {!transactions || transactions.length === 0 ? (
          <tr>
            <td colSpan="10" className="text-center py-4 text-gray-500">
              تراکنشی یافت نشد
            </td>
          </tr>
        ) : (
          transactions.map((t) => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>{t.customer_name || "-"}</td>
              <td>{t.customer_phone || "-"}</td>
              <td>{t.card_name || "-"}</td>
              <td>{t.buy_price || "-"}</td>
              <td>{t.sell_price || "-"}</td>
              <td>{t.amount}</td>
              <td>{t.is_successful ? "موفق" : "ناموفق"}</td>
              <td>{t.is_settled ? "تسویه شده" : "تسویه نشده"}</td>
              <td
                style={{
                  color: t.debt_or_credit_type === "debt" ? "red" : "green",
                }}
              >
                {t.debt_or_credit || "-"}
              </td>
            </tr>
          ))
        )}
      </tbody>
    </table>
  );
};

export default TransactionTable;
