
import React, { useEffect, useState } from 'react';
import api from '../api/axios';

export default function TransactionForm({ onCreated }) {
  const [amount, setAmount] = useState('');
  const [date, setDate] = useState(() => new Date().toISOString().slice(0,10));
  const [description, setDescription] = useState('');
  const [currencies, setCurrencies] = useState([]);
  const [categories, setCategories] = useState([]);
  const [currencyId, setCurrencyId] = useState('');
  const [categoryId, setCategoryId] = useState('');

  useEffect(() => {
    (async () => {
      const [curs, cats] = await Promise.all([
        api.get('core/currencies/'),
        api.get('core/categories/'),
      ]);
      setCurrencies(curs.data || []);
      setCategories(cats.data || []);
      if (curs.data?.length) setCurrencyId(curs.data[0].id);
    })();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    const payload = {
      amount: parseFloat(amount),
      date,
      description,
      currency: currencyId || null,
      category: categoryId || null,
    };
    const r = await api.post('transactions/', payload);
    setAmount(''); setDescription('');
    onCreated?.(r.data);
  };

  return (
    <form onSubmit={submit} className="p-4 rounded-xl border shadow bg-white">
      <h3 className="text-lg font-semibold mb-3">Add Transaction</h3>
      <div className="grid grid-cols-6 gap-3 items-end">
        <div className="col-span-2">
          <label className="block text-sm text-gray-600 mb-1">Amount</label>
          <input required type="number" step="0.01" className="border rounded px-2 py-1 w-full" value={amount} onChange={e=>setAmount(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm text-gray-600 mb-1">Currency</label>
          <select className="border rounded px-2 py-1 w-full" value={currencyId} onChange={e=>setCurrencyId(e.target.value)}>
            {currencies.map(c => <option key={c.id} value={c.id}>{c.code}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm text-gray-600 mb-1">Category</label>
          <select className="border rounded px-2 py-1 w-full" value={categoryId} onChange={e=>setCategoryId(e.target.value)}>
            <option value="">Undefined (expense)</option>
            {categories.map(c => <option key={c.id} value={c.id}>{c.name} {c.is_income ? '(Income)' : ''}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm text-gray-600 mb-1">Date</label>
          <input type="date" className="border rounded px-2 py-1 w-full" value={date} onChange={e=>setDate(e.target.value)} />
        </div>
        <div className="col-span-6">
          <label className="block text-sm text-gray-600 mb-1">Description</label>
          <input className="border rounded px-2 py-1 w-full" value={description} onChange={e=>setDescription(e.target.value)} />
        </div>
        <div className="col-span-6 flex justify-end">
          <button className="px-4 py-2 rounded bg-blue-600 text-white">Add</button>
        </div>
      </div>
    </form>
  );
}
