import { useEffect, useState } from "react";
import { getLatestPrice, setPrice } from "@/services/transferAndRanges";
import toast from "react-hot-toast";

const usePriceManager = () => {
  const [originalBuyPrice, setOriginalBuyPrice] = useState(null);
  const [originalSellPrice, setOriginalSellPrice] = useState(null);
  const [inputBuyPrice, setInputBuyPrice] = useState("");
  const [inputSellPrice, setInputSellPrice] = useState("");
  const [loading, setLoading] = useState(true);
  const [showEditPrices, setShowEditPrices] = useState(false);

  useEffect(() => {
    getLatestPrice()
      .then((data) => {
        setOriginalBuyPrice(data.buy_price ?? "");
        setOriginalSellPrice(data.sell_price ?? "");
        setInputBuyPrice(data.buy_price ?? "");
        setInputSellPrice(data.sell_price ?? "");
      })
      .catch(() => {
        toast.error("خطا در بارگذاری قیمت‌ها");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleBuyPriceSave = async () => {
    if (inputBuyPrice === "" || isNaN(Number(inputBuyPrice))) {
      toast.error("لطفاً قیمت خرید را به صورت عددی وارد کنید");
      return;
    }
    try {
      await setPrice({
        buy_price: Number(inputBuyPrice),
        sell_price:
          originalSellPrice !== "" ? Number(originalSellPrice) : undefined,
      });
      toast.success("قیمت خرید با موفقیت ذخیره شد");
      setOriginalBuyPrice(inputBuyPrice);
    } catch (error) {
      console.error("BuyPriceSave error detail:", error.response?.data || error);
      toast.error("خطا در ذخیره قیمت خرید");
    }
  };

  const handleSellPriceSave = async () => {
    if (inputSellPrice === "" || isNaN(Number(inputSellPrice))) {
      toast.error("لطفاً قیمت فروش را به صورت عددی وارد کنید");
      return;
    }
    try {
      await setPrice({
        sell_price: Number(inputSellPrice),
        buy_price:
          originalBuyPrice !== "" ? Number(originalBuyPrice) : undefined,
      });
      toast.success("قیمت فروش با موفقیت ذخیره شد");
      setOriginalSellPrice(inputSellPrice);
    } catch (error) {
      console.error("SellPriceSave error detail:", error.response?.data || error);
      toast.error("خطا در ذخیره قیمت فروش");
    }
  };

  return {
    loading,
    originalBuyPrice,
    originalSellPrice,
    inputBuyPrice,
    inputSellPrice,
    showEditPrices,
    setShowEditPrices,
    setInputBuyPrice,
    setInputSellPrice,
    handleBuyPriceSave,
    handleSellPriceSave,
  };
};

export default usePriceManager;