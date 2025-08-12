// frontend/src/services/transactionControlService.js
import api from "./api";

const RESOURCE = "/transaction-status";

export const getTransactionControl = () => {
  return api.get(RESOURCE);
};

/**
 * ارسال patch برای به‌روزرسانی یکی یا هر دو فیلد.
 * دریافت پارامتر به شکل شیء: { buying_disabled, selling_disabled }
 */
export const updateTransactionControl = ({ buying_disabled, selling_disabled } = {}) => {
  const payload = {};
  if (typeof buying_disabled !== "undefined") payload.buying_disabled = buying_disabled;
  if (typeof selling_disabled !== "undefined") payload.selling_disabled = selling_disabled;

  return api.patch(RESOURCE, payload);
};

/**
 * کمکی برای چک کردن اینکه آیا نوع تراکنش مجاز هست یا نه
 * type: "buying" | "selling"
 */
export const isTransactionAllowed = async (type) => {
  const res = await getTransactionControl();
  const { buying_disabled, selling_disabled } = res.data;
  if (type === "buying") return !buying_disabled;
  if (type === "selling") return !selling_disabled;
  return false;
};
