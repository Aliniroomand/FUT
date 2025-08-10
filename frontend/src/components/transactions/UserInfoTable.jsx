import user_labels from "@/constants/user_infos_labels";

const UserInfoTable = ({ user }) => {
  if (!user) return null;
  return (
    <table className="min-w-full border border-yellow-500 rounded-lg text-yellow-400 my-2 bg-yellow-950  ">
      <tbody>
        {Object.entries(user).map(([key, value]) => (
          <tr key={key} className="odd:bg-blue-900/20 even:bg-blue-900/10">
            <td className="py-2 px-4 border-b border-yellow-700 font-semibold text-shadow-black w-1/3">
              {user_labels[key] || key}
            </td>
            <td className="py-2 px-4 border-b border-yellow-700 text-yellow-300 w-2/3">
              {value?.toString() || "-"}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default UserInfoTable;
