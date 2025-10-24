
import React from "react";

const DEFAULT_GRAY = "#9CA3AF";
const CAT_COLORS = [
  "#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#a4de6c",
  "#8dd1e1", "#d0ed57", "#83a6ed", "#ffbb28", "#ff7f50"
];

export default function BudgetProgress({ items, colorsByCategory }) {
  if (!items || !items.length) return null;

  const colorForCategory = (name, i) =>
    (colorsByCategory && colorsByCategory[name]) ||
    CAT_COLORS[i % CAT_COLORS.length] ||
    DEFAULT_GRAY;

  return (
    <div className="bg-white rounded-xl p-4 shadow-sm">
      <h3 className="text-lg font-semibold mb-3">Budgets</h3>
      <div className="space-y-3">
        {items.map((b, i) => {
          const limit = Number(b.limit || 0);
          const spent = Number(b.spent || 0);
          const progress = limit > 0 ? Math.min(1, Math.max(0, spent / limit)) : 0;
          const month = b.month;
          const cur = b.currency || "";
          const color = colorForCategory(b.category, i);

          return (
            <div key={i}>
              <div className="flex items-center justify-between mb-1">
                <span className="font-medium" style={{ color }}>
                  {b.category} — {month}
                </span>
                <span className="tabular-nums">
                  {spent.toFixed(2)} / {limit.toFixed(2)} {cur}
                </span>
              </div>
              <div className="w-full h-2 bg-gray-200 rounded">
                <div
                  className="h-2 rounded"
                  style={{ width: `${Math.round(progress * 100)}%`, backgroundColor: color }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
