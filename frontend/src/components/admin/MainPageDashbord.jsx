import React from "react";
import { Link } from "react-router-dom";

// Project components (uses your uploaded paths)
import PriceManager from "@/components/admin/PriceManager";
import TransactionsControl from "@/components/admin/TransactionsControl";
import LiveAlertsAndPendingTxs from "@/components/admin/Alerts/LiveAlertsAndPendingTxs";
import AdminEAAccountPanel from "@/components/admin/EAAcountsManagement/AdminEAAccountPanel";
import PlayerManagement from "@/components/admin/PlayerManagement/PlayerManagement";
import TransferMethod from "@/components/admin/TransferMethod";
import RangeManagement from "@/components/admin/RangeManagement/RangeManagement";
import MakeAdmin from "@/components/admin/MakeAdmin";
import ShowLivePrice from "@/components/Show_live_price";

// Simple, compact single-page dashboard
const COMPONENT_REGISTRY = [
  { key: "live_price", title: "قیمت زنده", Comp: ShowLivePrice, colSpan: 3, route: "/admin/live-price" },

  { key: "transactions", title: "تراکنش‌ها", Comp: TransactionsControl, colSpan: 6 },
  { key: "alerts", title: "نوتیفیکیشن‌ها", Comp: LiveAlertsAndPendingTxs, colSpan: 3 },

  { key: "ea_accounts", title: " ea اکانتهای", Comp: AdminEAAccountPanel, colSpan: 3 , route: "/admin/ea-accounts"},
  { key: "players", title: "مدیریت بازیکنان", Comp: PlayerManagement, colSpan: 6, route: "/admin/players" },

  { key: "transfer_methods", title: "روش‌های انتقال", Comp: TransferMethod, colSpan: 3, route: "/admin/transfer-methods" },
  { key: "range_mgmt", title: "قوانین بازه", Comp: RangeManagement, colSpan: 3, route: "/admin/range-management" },
  { key: "make_admin", title: "ابزار ادمین", Comp: MakeAdmin, colSpan: 3, route: "/admin/tools" }
];

export default function AdminDashboard({ registry = COMPONENT_REGISTRY }) {
  const headerFooterHeight = 96; 
  const linkKeys = new Set(["players", "transfer_methods", "range_mgmt", "make_admin","ea_accounts"]);

  return (
    <div className="sm:block hidden h-screen w-full p-3 overflow-hidden glass-dark" data-theme="fut-admin">

      <header className="flex items-center justify-center mb-2 h-14">
        <div className="self-center">
          <h1 className="text-lg font-extrabold text-center " >پنل مدیریت — داشبورد</h1>
          <p className="text-xs text-gray-400">نمایش فشرده — همه چیز در یک صفحه</p>
        </div>
      </header>

      <main
        style={{
          height: `calc(100vh - ${headerFooterHeight}px)`,
          display: "grid",
          gridTemplateColumns: "repeat(12, 1fr)",
          gridTemplateRows: "repeat(3, 1fr)",
          gap: "8px"
        }}
      >
        {registry.map((item) => {
          const Comp = item.Comp;
          const col = Math.min(12, item.colSpan || 3);
          const route = item.route || `/admin/${item.key}`;

          return (
            <section key={item.key} style={{ gridColumn: `auto / span ${col}`, overflow: "hidden" }}>
              <div className="panel h-full flex flex-col glass-light p-2" style={{ minHeight: 0 }}>
                <div className="flex items-center justify-between mb-2 ">
                  <h3 className="font-extrabold">{item.title}</h3>
                </div>

                <div className="flex-1 min-h-0 overflow-auto">
                  {linkKeys.has(item.key) ? (
                    <div className="h-full flex items-center justify-center  rounded-2xl">
                      <Link to={route} className="px-3 py-2 rounded-lg glass-light text-amber-900 " >
                        باز کردن {item.title}
                      </Link>
                    </div>
                  ) : Comp ? (
                    <Comp compact />
                  ) : (
                    <div className="text-xs text-gray-400 ">کامپوننت یافت نشد</div>
                  )}
                </div>
              </div>
            </section>
          );
        })}
      </main>

    </div>
  );
}
