




function AccountTable({ accounts, editId, editLimit, setEditId, setEditLimit, onEdit, onSave, onDelete, loading }) {
    const statusColor = {
      active: "text-green-500",
      paused: "text-yellow-400",
      banned: "text-red-500",
    };
    
    
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-dark-hard rounded-lg shadow">
        <thead>
          <tr className="bg-dark-soft text-amber-400 text-nowrap">
            <th className="py-2 px-4">نام</th>
            <th className="py-2 px-4">ایمیل</th>
            <th className="py-2 px-4">پلتفرم</th>
            <th className="py-2 px-4">سقف روزانه</th>
            <th className="py-2 px-4">انتقال امروز</th>
            <th className="py-2 px-4">وضعیت</th>
            <th className="py-2 px-4">ویرایش سقف انتقال</th>
            <th className="py-2 px-4">حذف</th>
            <th className="py-2 px-4">میزان تکمیل اکانت</th>
          </tr>
        </thead>
        <tbody>
          {accounts?.map((acc) => {
            const limit = acc.daily_limit || 1000000;
            const percent = Math.min(100, (acc.transferred_today / limit) * 100);
            return (
              <tr key={acc.id} className="border-b border-dark-soft">
                <td className="py-2 px-4">{acc.name}</td>
                <td className="py-2 px-4">{acc.email}</td>
                <td className="py-2 px-4">{acc.platform}</td>
                <td className="py-2 px-4">
                  {editId === acc.id ? (
                    <input
                      type="number"
                      value={editLimit || ""}
                      onChange={(e) => setEditLimit(e.target.value ? Number(e.target.value) : null)}
                      className="p-1 rounded border border-amber-400 bg-dark-hard text-white w-20"
                    />
                  ) : (
                    acc.daily_limit || <span className="text-xs text-gray-400">GLOBAL</span>
                  )}
                </td>
                <td className="py-2 px-4">{acc.transferred_today}</td>
                <td className={`py-2 px-4 font-bold ${statusColor[acc.status] || "text-gray-400"}`}>{acc.status}</td>
                <td className="py-2 px-4">
                  {editId === acc.id ? (
                    <button onClick={() => onSave(acc.id)} disabled={loading} className="bg-amber-400 text-dark-hard px-3 py-1 rounded shadow hover:bg-amber-500">ذخیره</button>
                  ) : (
                    <button onClick={() => onEdit(acc.id, acc.daily_limit || 0)} className="bg-dark-soft text-amber-400 border border-amber-400 px-3 py-1 rounded shadow hover:bg-amber-500 hover:text-white">ویرایش</button>
                  )}
                </td>
                <td className="py-2 px-4">
                  <button onClick={() => onDelete(acc.id)} disabled={loading} className="bg-red-400 text-white px-3 py-1 rounded shadow hover:bg-red-500">حذف</button>
                </td>
                <td className="py-2 px-4">
                  <div className="w-32 h-3 bg-gray-700 rounded">
                    <div className="h-3 rounded bg-amber-400" style={{ width: `${percent}%` }}></div>
                  </div>
                  <span className="text-xs text-gray-300 ml-2">{percent.toFixed(1)}%</span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
export default AccountTable