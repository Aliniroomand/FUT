import React from "react";
import AlertItem from "./AlertItem";
const SolvedAlertsList = React.memo(({ solvedAlerts }) => {
  return (
    <>
      <h2 className="text-xl font-bold mt-8 mb-4 text-green-400">
        هشدارهای حل‌شده طی 24 ساعت اخیر
      </h2> 
      {solvedAlerts.length === 0 && (
        <div className="text-gray-500">هشدار حل‌شده‌ای وجود ندارد</div>
      )}
      <div className="space-y-3 mt-3">
        {solvedAlerts.map((a) => (
          <AlertItem key={a.id} alert={a} resolved={true} />
        ))}
      </div>
    </>
  );
});
export default SolvedAlertsList
