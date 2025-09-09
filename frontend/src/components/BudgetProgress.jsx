import React from "react";

export default function BudgetProgress({ items }) {
  if (!items || !items.length) return null;
  return (
    <div className="bg-white rounded-xl p-4 shadow-sm">
      <h3 className="text-lg font-semibold mb-3">Budgets</h3>
      <div className="space-y-3">
        {items.map((b) => (
          <div key={b.category + b.month}>
            <div className="flex justify-between text-sm mb-1">
              <span>{b.category} — {b.month}</span>
              <span>{b.spent.toFixed(2)} / {b.limit.toFixed(2)} {b.currency}</span>
            </div>
            <div className="w-full h-2 bg-gray-200 rounded">
              <div className="h-2 rounded" style={{ width: `${Math.min(100, Math.round((b.progress||0)*100))}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
