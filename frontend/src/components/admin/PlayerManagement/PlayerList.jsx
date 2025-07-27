export default function PlayerList({ players, onEdit, onDelete }) {
  if (players.length === 0) {
    return <div className="text-gray-400 text-center py-4">هیچ بازیکنی ایجاد نشده است</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-700">
        <thead className="bg-gray-700">
          <tr>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">نام</th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">باشگاه</th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">رتبه</th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">ورژن</th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">عملیات</th>
          </tr>
        </thead>
        <tbody className="bg-gray-800 divide-y divide-gray-700">
          {players.map(player => (
            <tr key={player.id}>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-white">{player.name}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">{player.club}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-amber-400">{player.rating}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">{player.version}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm font-medium">
                <div className="flex gap-2">
                  <button
                    onClick={() => onEdit(player)}
                    className="text-amber-500 hover:text-amber-400"
                  >
                    ویرایش
                  </button>
                  <button
                    onClick={() => onDelete(player.id)}
                    className="text-red-500 hover:text-red-400"
                  >
                    حذف
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}