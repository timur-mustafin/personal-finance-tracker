import React from "react";

const CAT_COLORS = [
  "#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#a4de6c",
  "#8dd1e1", "#d0ed57", "#83a6ed", "#ffbb28", "#ff7f50"
];

export default function BudgetProgress({ items }) {
  if (!items || !items.length) return null;
  const colorFor = (i) => CAT_COLORS[i % CAT_COLORS.length];
  return (
    <div className="bg-white rounded-xl p-4 shadow-sm">
      <h3 className="text-lg font-semibold mb-3">Budgets</h3>
      <div className="space-y-3">
        {items.map((b, i) => {
          const limit = Number(b.limit || 0);
          const spent = Number(b.spent || 0);
          const progress = Number.isFinite(b.progress) ? b.progress : (limit > 0 ? spent/limit : 0);
          const month = b.month || new Date().toISOString().slice(0,7);
          const cur = b.currency || "";
          return (
            <div key={(b.category||'cat') + month}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium" style={{color: colorFor(i)}}>
                  {b.category} — {month}
                </span>
                <span className="tabular-nums">{spent.toFixed(2)} / {limit.toFixed(2)} {cur}</span>
              </div>
              <div className="w-full h-2 bg-gray-200 rounded">
                <div className="h-2 rounded" style={{ width: `${Math.min(100, Math.round(progress*100))}%`, backgroundColor: colorFor(i) }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
