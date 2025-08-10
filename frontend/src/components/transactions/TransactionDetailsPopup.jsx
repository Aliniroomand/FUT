// src/components/TransactionDetailsPopup.jsx
import transfer_labels from "@/constants/transfers_labels";
import StatusIcon from "@/helper/StatusIcon";
import ToggleButton from "@/helper/ToggleBTN";
import { getPlayerCard } from "@/services/playerCardsApi";
import { getUserById } from "@/services/usersApi"; // فرض بر اینکه این API دارید
import { getTransferMethodById } from "@/services/transferMethodsApi";
import UserInfoTable from "./UserInfoTable";
import { useEffect, useState } from "react";

const TransactionDetailsPopup = ({ transaction, onClose, onToggleSettled }) => {
  const [cardInfo, setCardInfo] = useState(null);
  const [userInfo, setUserInfo] = useState(null);
  const [transferMethod, setTransferMethod] = useState(null);

  // دریافت اطلاعات کارت
  useEffect(() => {
    if (transaction?.card_id) {
      getPlayerCard(transaction.card_id)
        .then(setCardInfo)
        .catch(() => setCardInfo(null));
    }
  }, [transaction?.card_id]);

  // دریافت اطلاعات کاربر
  useEffect(() => {
    if (transaction?.user_id) {
      getUserById(transaction.user_id)
        .then(setUserInfo)
        .catch(() => setUserInfo(null));
    }
  }, [transaction?.user_id]);

  // دریافت اطلاعات روش انتقال
  useEffect(() => {
    if (transaction?.transfer_method_id) {
      getTransferMethodById(transaction.transfer_method_id)
        .then(setTransferMethod)
        .catch(() => setTransferMethod(null));
    }
  }, [transaction?.transfer_method_id]);

  if (!transaction) return null;

  const bgColor =
    transaction.is_successful === 1 ? "bg-green-900/50" : "bg-red-900/50";

  return (
    <div
      className={`fixed inset-0 flex justify-center items-center z-50 h-[90svh] top-[9%] m-auto overflow-y-auto p-4 backdrop-blur-3xl w-fit `}

    >
      <div className={`flex-col justify-around gap-4 h-full rounded-lg shadow-lg w-full max-w-3xl text-amber-400 top-0 bg-black/40 p-6 overflow-y-scroll backf`}>
        <h2 className="text-3xl font-bold text-amber-400 drop-shadow-lg mb-5">
          جزئیات تراکنش
        </h2>
        <table className={`min-w-full  border border-amber-700 rounded-lg text-amber-200 overflow-scroll ${bgColor} `}>
          <tbody>
            {Object.entries(transaction).map(([key, value]) => {
              // نمایش اطلاعات جایگزین برای شناسه‌ها
              if (key === "card_id") {
                return (
                  <tr
                    key={key}
                    className="odd:bg-amber-900/20 even:bg-amber-900/10"
                  >
                    <td className="py-3 px-5 border-b border-amber-700 font-semibold text-shadow-black">
                      {transfer_labels[key] || key}
                    </td>
                    <td className="py-3 px-5 border-b border-amber-700 text-amber-300">
                      {cardInfo ? (
                        <>
                          {cardInfo.name} ({cardInfo.position} - {cardInfo.club})
                        </>
                      ) : (
                        "در حال بارگذاری..."
                      )}
                    </td>
                  </tr>
                );
              }

              if (key === "user_id") {
                return (
                  <tr key={key} className="odd:bg-amber-900/20 even:bg-amber-900/10">
                    <td className="py-3 px-5 border-b border-amber-700 font-semibold text-shadow-black">
                      {transfer_labels[key] || key}
                    </td>
                    <td className="py-3 px-5 border-b border-amber-700 text-amber-300">
                      {userInfo ? (
                        <UserInfoTable user={userInfo} />
                      ) : (
                        "در حال بارگذاری..."
                      )}
                    </td>
                  </tr>
                );
              }

              if (key === "transfer_method_id") {
                return (
                  <tr key={key} className="odd:bg-amber-900/20 even:bg-amber-900/10">
                    <td className="py-3 px-5 border-b border-amber-700 font-semibold text-shadow-black">
                      {transfer_labels[key] || key}
                    </td>
                    <td className="py-3 px-5 border-b border-amber-700 text-amber-300">
                      {transferMethod ? transferMethod.name : "در حال بارگذاری..."}
                    </td>
                  </tr>
                );
              }

              if (key === "is_successful") {
                return (
                  <tr
                    key={key}
                    className="odd:bg-amber-900/20 even:bg-amber-900/10 "
                  >
                    <td className=" border-b border-amber-700 font-semibold text-shadow-black">
                      {transfer_labels[key] || key}
                    </td>
                    <td className="py-3 px-5 border-b border-amber-700 text-amber-300 grid place-items-center ">
                      <StatusIcon status={value} />
                    </td>
                  </tr>
                );
              }

              if (key === "is_settled") {
                return (
                  <tr
                    key={key}
                    className="odd:bg-amber-900/20 even:bg-amber-900/10"
                  >
                    <td className="py-3 px-5 border-b border-amber-700 font-semibold text-shadow-black">
                      {transfer_labels[key] || key}
                    </td>
                    <td className="py-3 px-5 border-b border-amber-700 text-amber-300">
                      <ToggleButton
                        value={Boolean(value)}
                        onChange={(newVal) => onToggleSettled(transaction.id, newVal)}
                      />
                    </td>
                  </tr>
                );
              }

              // رندر معمولی بقیه فیلدها
              return (
                <tr
                  key={key}
                  className="odd:bg-amber-900/20 even:bg-amber-900/10"
                >
                  <td className="py-3 px-5 border-b border-amber-700 font-semibold text-shadow-black">
                    {transfer_labels[key] || key}
                  </td>
                  <td className="py-3 px-5 border-b border-amber-700 text-amber-300">
                    {value?.toString()}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <button
        onClick={onClose}
        className="absolute text-black text-3xl top-0 right-0 px-5 py-2 bg-amber-500 text-dark-hard font-semibold rounded-full hover:bg-amber-600 transition-shadow shadow-lg"
      >
        x
      </button>
    </div>
  );
};

export default TransactionDetailsPopup;
