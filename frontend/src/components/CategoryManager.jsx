
import React, { useEffect, useState } from 'react';
import api from '../api/axios';

function CategoryRow({ cat, onSave, onDelete }) {
  const [edit, setEdit] = useState(false);
  const [name, setName] = useState(cat.name);
  const [isIncome, setIsIncome] = useState(!!cat.is_income);
  const [color, setColor] = useState(cat.color || '#9CA3AF');

  const save = async () => {
    const payload = { name, is_income: isIncome, color };
    const r = await api.put(`core/categories/${cat.id}/`, payload);
    onSave(r.data);
    setEdit(false);
  };
  const del = async () => {
    if (!confirm(`Delete category "${cat.name}"? Its transactions will become Undefined.`)) return;
    await api.delete(`core/categories/${cat.id}/`);
    onDelete(cat.id);
  };

  return (
    <tr className="border-b">
      <td className="p-2">
        {edit ? <input className="border rounded px-2 py-1 w-full" value={name} onChange={e=>setName(e.target.value)} /> : name}
      </td>
      <td className="p-2 text-center">
        {edit ? <input type="color" value={color} onChange={e=>setColor(e.target.value)} /> : <span className="inline-block w-4 h-4 rounded" style={{background: color}} />}
      </td>
      <td className="p-2 text-center">{edit ? <input type="checkbox" checked={isIncome} onChange={e=>setIsIncome(e.target.checked)} /> : (isIncome ? 'Income' : 'Expense')}</td>
      <td className="p-2 text-right space-x-2">
        {edit ? (
          <>
            <button className="px-2 py-1 rounded bg-gray-200" onClick={()=>setEdit(false)}>Cancel</button>
            <button className="px-2 py-1 rounded bg-blue-600 text-white" onClick={save}>Save</button>
          </>
        ) : (
          <>
            <button className="px-2 py-1 rounded bg-gray-200" onClick={()=>setEdit(true)}>Edit</button>
            <button className="px-2 py-1 rounded bg-red-600 text-white" onClick={del}>Delete</button>
          </>
        )}
      </td>
    </tr>
  );
}

export default function CategoryManager() {
  const [cats, setCats] = useState([]);
  const [name, setName] = useState('');
  const [color, setColor] = useState('#9CA3AF');
  const [isIncome, setIsIncome] = useState(false);

  const load = async () => {
    const r = await api.get('core/categories/');
    setCats(r.data || []);
  };
  useEffect(() => { load(); }, []);

  const add = async () => {
    if (!name.trim()) return;
    const payload = { name: name.trim(), is_income: isIncome, color };
    const r = await api.post('core/categories/', payload);
    setCats([r.data, ...cats]);
    setName('');
  };

  const onSave = (changed) => {
    setCats(cats.map(c => c.id === changed.id ? changed : c));
  };
  const onDelete = (id) => {
    setCats(cats.filter(c => c.id !== id));
  };

  return (
    <div className="p-4 rounded-xl border shadow bg-white">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold">Categories</h3>
      </div>
      <div className="flex items-center gap-2 mb-3">
        <input className="border rounded px-2 py-1 flex-1" placeholder="New category name…" value={name} onChange={e=>setName(e.target.value)} />
        <label className="flex items-center gap-2 text-sm">
          <span>Color</span>
          <input type="color" value={color} onChange={e=>setColor(e.target.value)} />
        </label>
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={isIncome} onChange={e=>setIsIncome(e.target.checked)} />
          <span>Income</span>
        </label>
        <button className="px-3 py-2 rounded bg-emerald-600 text-white" onClick={add}>Add</button>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left">
            <th className="p-2">Name</th>
            <th className="p-2 text-center">Color</th>
            <th className="p-2 text-center">Type</th>
            <th className="p-2 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {cats.map(c => <CategoryRow key={c.id} cat={c} onSave={onSave} onDelete={onDelete} />)}
        </tbody>
      </table>
      <p className="text-xs text-gray-500 mt-2">Deleting a category will set existing transactions to <strong>Undefined</strong> (gray) on the dashboard.</p>
    </div>
  );
}
