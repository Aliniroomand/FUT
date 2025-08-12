// frontend/src/components/admin/TransactionControlButton.jsx
import React, { useEffect, useState } from "react";
import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";
import { toast } from "react-hot-toast";
import {
  getTransactionControl,
  updateTransactionControl,
} from "@/services/transactionsControlApi";

/**
 * یک دکمه برای روشن/خاموش کردن خرید و فروش به‌صورت جداگانه
 */
export default function TransactionControlButton() {
  const [control, setControl] = useState({
    buying_disabled: false,
    selling_disabled: false,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState({ buying: false, selling: false });

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getTransactionControl()
      .then((res) => {
        if (!mounted) return;
        setControl(res.data || control);
      })
      .catch((err) => {
        console.error("fetch transaction-control:", err);
        toast.error("خطا در دریافت وضعیت تراکنش‌ها");
      })
      .finally(() => mounted && setLoading(false));
    return () => (mounted = false);
  }, []);

  const handleToggle = async (type) => {
    const newDisabledValue = !control[`${type}_disabled`]; // معکوس کردن مقدار فعلی

    const payload = {
      [`${type}_disabled`]: newDisabledValue,
    };

    try {
      setSaving((prev) => ({ ...prev, [type]: true }));
      const res = await updateTransactionControl(payload);

      if (res.status !== 200) {
        throw new Error(`Failed to update ${type}`);
      }

      setControl((prev) => ({
        ...prev,
        [`${type}_disabled`]: newDisabledValue, // به‌روزرسانی مقدار جدید در حالت
      }));

      toast.success(
        `وضعیت ${type === "buying" ? "خرید" : "فروش"} با موفقیت بروزرسانی شد`
      );
    } catch (err) {
      console.error(`update transaction-control (${type}):`, err);
      toast.error(
        `خطا در ذخیره تغییرات ${type === "buying" ? "خرید" : "فروش"}`
      );
    } finally {
      setSaving((prev) => ({ ...prev, [type]: false }));
    }
  };

  return (
    <div className="flex flex-col-reverse items-center gap-3 glass-dark p-4 rounded-4xl">
      <div className="flex w-2/3  ">
        {/* Toggle for Buying */}
        <button
          onClick={() => handleToggle("buying")}
          disabled={loading || saving.buying}
          className={`flex items-center gap-2 px-4 py-2 rounded-md border transition-colors select-none w-1/2 text-base 
          ${
            !control.buying_disabled
              ? "border-green-300 hover:bg-green-50  bg-green-200"
              : "border-red-300 hover:bg-red-50 bg-red-100 "
          }
          ${
            loading || saving.buying
              ? "opacity-60 cursor-not-allowed"
              : "cursor-pointer"
          }
          `}
          aria-pressed={!control.buying_disabled}
        >
          {!control.buying_disabled ? (
            <>
              <FaCheckCircle className="text-green-500" />
              <span className=" text-green-700">خرید فعال است</span>
            </>
          ) : (
            <>
              <FaTimesCircle className="text-red-500" />
              <span className=" text-red-700">خرید غیر فعال شده</span>
            </>
          )}
        </button>

        {/* Toggle for Selling */}
        <button
          onClick={() => handleToggle("selling")}
          disabled={loading || saving.selling}
          className={`flex items-center gap-2 px-4 py-2 rounded-md border transition-colors select-none w-1/2 text-base
          ${
            !control.selling_disabled
              ? "border-green-300 hover:bg-green-50 bg-green-200"
              : "border-red-300 hover:bg-red-50 bg-red-100"
          }
          ${
            loading || saving.selling
              ? "opacity-60 cursor-not-allowed "
              : "cursor-pointer"
          }
          `}
          aria-pressed={!control.selling_disabled}
        >
          {!control.selling_disabled ? (
            <>
              <FaCheckCircle className="text-green-500 " />
              <span className=" text-green-700 ">فروش فعال است</span>
            </>
          ) : (
            <>
              <FaTimesCircle className="text-red-500" />
              <span className=" text-red-700">فروش غیر فعال شده</span>
            </>
          )}
        </button>
      </div>

        <div className="text-md text-white-500 shadow-2xl">
          با کلیک، خرید یا فروش به‌صورت جداگانه فعال/غیرفعال می‌شود.
        </div>
    </div>
  );
}
