import React from "react";
import axios from "axios";

const CreateTestTransactions = () => {
  const createTransactions = async () => {
    const api ="http://localhost:8000"


    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("توکن دسترسی موجود نیست. لطفا ابتدا وارد شوید.");
      return;
    }

    const testData = [
      {
        user_id: 1,
        card_id: 10,
        transfer_method_id: 1,
        amount: 5000,
        transaction_type: "buy",
        is_successful: 1,
        is_settled: 0,
        buy_price: 1000,
        sell_price: 1200,
        customer_phone: "09123456789",
        customer_email: "test1@example.com",
        debt_or_credit: 200,
        debt_or_credit_type: "credit",
        transfer_multiplier: 1.0,
      },
      {
        user_id: 1,
        card_id: 11,
        transfer_method_id: 2,
        amount: 3000,
        transaction_type: "sell",
        is_successful: 0,
        is_settled: 0,
        buy_price: 800,
        sell_price: 900,
        customer_phone: "09129876543",
        customer_email: "test2@example.com",
        debt_or_credit: 100,
        debt_or_credit_type: "debt",
        transfer_multiplier: 0.9,
      },
      // در صورت نیاز تراکنش‌های بیشتری اضافه کنید
    ];

    try {
      for (const tx of testData) {
        const res = await axios.post(`/${api}/transactions/`, tx, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log("تراکنش ساخته شد:", res.data);
      }
      alert("تراکنش‌های تستی با موفقیت ساخته شدند.");
    } catch (error) {
      console.error("خطا در ساخت تراکنش‌ها:", error);
      alert("خطا در ساخت تراکنش‌ها. لطفا کنسول را بررسی کنید.");
    }
  };

  return (
    <div>
      <button
        onClick={createTransactions}
        className="btn btn-primary"
        type="button"
      >
        ساخت تراکنش‌های تستی
      </button>
    </div>
  );
};

export default CreateTestTransactions;
