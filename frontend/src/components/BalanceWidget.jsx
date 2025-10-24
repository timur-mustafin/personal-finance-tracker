
import React, { useEffect, useState } from 'react';
import api from '../api/axios';

export default function BalanceWidget() {
  const [balances, setBalances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    api.get('transactions/balances/')
      .then(r => { if (mounted) { setBalances(r.data.balances || []); setLoading(false); } })
      .catch(e => { if (mounted) { setError(e?.response?.data || e.message); setLoading(false); } });
    return () => { mounted = false; }
  }, []);

  if (loading) return <div className="p-4 rounded-lg border shadow-sm">Loading balances…</div>;
  if (error) return <div className="p-4 rounded-lg border shadow-sm text-red-600">Failed to load: {String(error)}</div>;

  const order = ['USD','EUR','RSD'];
  const sorted = [...balances].sort((a,b) => order.indexOf(a.currency) - order.indexOf(b.currency));

  return (
    <div className="p-4 rounded-xl border shadow bg-white">
      <h3 className="text-lg font-semibold mb-3">Current Balance</h3>
      <div className="grid grid-cols-3 gap-4">
        {sorted.map((b,i) => (
          <div key={i} className="rounded-lg border p-3">
            <div className="text-sm text-gray-500">{b.currency}</div>
            <div className="text-2xl font-bold">{b.balance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
