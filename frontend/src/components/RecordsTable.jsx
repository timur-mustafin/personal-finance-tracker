
import React, { useEffect, useState } from 'react';
import api from '../api/axios';

export default function RecordsTable() {
  const [rows, setRows] = useState([]);
  const [cats, setCats] = useState({});
  const [curs, setCurs] = useState({});

  const load = async () => {
    const [txs, categories, currencies] = await Promise.all([
      api.get('transactions/'),
      api.get('core/categories/'),
      api.get('core/currencies/'),
    ]);
    setRows(txs.data || []);
    setCats(Object.fromEntries((categories.data||[]).map(c=>[c.id, c])));
    setCurs(Object.fromEntries((currencies.data||[]).map(c=>[c.id, c])));
  };
  useEffect(()=>{ load(); }, []);

  const save = async (id, patch) => {
    const r = await api.patch(`transactions/${id}/`, patch);
    setRows(rows.map(x => x.id === id ? r.data : x));
  };
  const del = async (id) => {
    if (!confirm('Delete this record?')) return;
    await api.delete(`transactions/${id}/`);
    setRows(rows.filter(x => x.id !== id));
  };

  return (
    <div className="p-4 rounded-xl border shadow bg-white">
      <h3 className="text-lg font-semibold mb-3">Records</h3>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left">
            <th className="p-2">Date</th>
            <th className="p-2">Amount</th>
            <th className="p-2">Cur</th>
            <th className="p-2">Category</th>
            <th className="p-2">Description</th>
            <th className="p-2 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => {
            const cat = r.category ? cats[r.category] : null;
            const cur = r.currency ? curs[r.currency] : null;
            return (
              <tr key={r.id} className="border-b">
                <td className="p-2"><input type="date" className="border rounded px-2 py-1" value={r.date} onChange={e=>save(r.id,{date:e.target.value})} /></td>
                <td className="p-2"><input type="number" step="0.01" className="border rounded px-2 py-1 w-32" value={r.amount} onChange={e=>save(r.id,{amount:e.target.value})} /></td>
                <td className="p-2">
                  <select className="border rounded px-2 py-1" value={r.currency || ''} onChange={e=>save(r.id,{currency:e.target.value})}>
                    {Object.values(curs).map(c => <option key={c.id} value={c.id}>{c.code}</option>)}
                  </select>
                </td>
                <td className="p-2">
                  <select className="border rounded px-2 py-1" value={r.category || ''} onChange={e=>save(r.id,{category:e.target.value || null})}>
                    <option value="">Undefined</option>
                    {Object.values(cats).map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                  </select>
                </td>
                <td className="p-2"><input className="border rounded px-2 py-1 w-full" value={r.description || ''} onChange={e=>save(r.id,{description:e.target.value})} /></td>
                <td className="p-2 text-right">
                  <button className="px-2 py-1 rounded bg-red-600 text-white" onClick={()=>del(r.id)}>Delete</button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
