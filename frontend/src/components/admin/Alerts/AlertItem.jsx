import React from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import { FaExclamationCircle } from "react-icons/fa";

dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);

const AlertItem = ({ alert, onResolve }) => {
  if (!alert.created_at) return null;

  // زمان به تایم تهران
  const tehranTime = dayjs(alert.created_at)
    .tz("Asia/Tehran")
    .format("HH:mm"); // ساعت و دقیقه

  // تاریخ شمسی (فارسی)
  const tehranDate = new Date(alert.created_at).toLocaleDateString("fa-IR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  // مدت زمان گذشته
  const fromNow = dayjs(alert.created_at).fromNow();

  return (
    <div className="border rounded-lg p-3 flex items-center justify-between glass-light">
      <div className="flex items-center justify-start  gap-7 ">
        <div className="text-red-600">
          <FaExclamationCircle size={30} />
        </div>
        <div className="font-bold bg-red-800 p-3 rounded-full">
          <span>نوع ارور :</span>
          <br />
          <span>{alert.type}</span>
        </div>
        <div className="text-base text-black bg-red-100 p-4 rounded-2xl">
          <span>پیام ارور</span>
          <span>{alert.message}</span>
        </div>
        <div className="text-sm text-yellow-900 bg-amber-300 mt-1 p-2 rounded">
          تایم ارور :<br />
          ساعت: {tehranTime}  <br /> {tehranDate} <br />
          time lapsed {fromNow}
        </div>
      </div>
      <div className="flex items-center gap-2">
        <button
          className="px-3 py-1 bg-green-600 text-white rounded"
          onClick={onResolve}
        >
          حل شد
        </button>
      </div>
    </div>
  );
};

export default AlertItem;
