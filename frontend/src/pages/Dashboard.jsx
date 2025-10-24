import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import BudgetProgress from '../components/BudgetProgress';
import CurrencySelector from '../components/CurrencySelector';
import BalanceWidget from '../components/BalanceWidget';
import CategoryManager from '../components/CategoryManager';
import TransactionForm from '../components/TransactionForm';
import RecordsTable from '../components/RecordsTable';

import { fmt2 } from '../utils/format';
const DEFAULT_GRAY = '#9CA3AF';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#a4de6c'];

  

/** Toast UI (same as before, with optional action button) */
function Toast({ id, type = 'info', title, message, actionLabel, onAction, onClose }) {
  const base =
    'pointer-events-auto w-80 rounded-lg shadow-lg p-4 text-sm mb-2 border backdrop-blur bg-white/95';
  const style =
    type === 'success'
      ? 'border-green-300'
      : type === 'error'
      ? 'border-red-300'
      : 'border-gray-300';

  useEffect(() => {
    const t = setTimeout(() => onClose(id), 5000);
    return () => clearTimeout(t);
  }, [id, onClose]);

  return (
    <div className={`${base} ${style}`}>
      <div className="flex items-start gap-2">
        <div
          className={`mt-1 h-2 w-2 rounded-full ${
            type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-gray-400'
          }`}
        />
        <div className="flex-1">
          {title && <div className="font-semibold mb-1">{title}</div>}
          {message && <div className="text-gray-700 whitespace-pre-wrap">{message}</div>}
          {actionLabel && onAction && (
            <button
              onClick={onAction}
              className="mt-2 inline-block bg-gray-800 hover:bg-gray-900 text-white px-3 py-1 rounded transition"
            >
              {actionLabel}
            </button>
          )}
        </div>
        <button
          onClick={() => onClose(id)}
          className="opacity-60 hover:opacity-100 transition text-gray-600"
          aria-label="Close"
          title="Close"
        >
          ×
        </button>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [categories, setCategories] = useState([]);
  useEffect(() => { (async () => { try { const r = await api.get('core/categories/'); setCategories(r.data || []); } catch(e) {} })(); }, []);

  const colorByCategory = useMemo(() => {
    const m = {};
    for (const c of categories) m[c.name] = c.color || DEFAULT_GRAY;
    m['Undefined'] = DEFAULT_GRAY;
    return m;
  }, [categories]);

  const [user, setUser] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);
  const [topCategories, setTopCategories] = useState([]);
  const [budgetsData, setBudgetsData] = useState([]);

  const [currency, setCurrency] = useState('USD');
  const [currencyOptions, setCurrencyOptions] = useState([]);
  const [csvFile, setCsvFile] = useState(null);
  const [busy, setBusy] = useState(false);

  const [toasts, setToasts] = useState([]);
  const navigate = useNavigate();

  const pushToast = useCallback((t) => {
    const id = Math.random().toString(36).slice(2);
    setToasts((prev) => [...prev, { id, ...t }]);
  }, []);
  const closeToast = useCallback((id) => {
    setToasts((prev) => {
      const found = prev.find((t) => t.id === id);
      if (found?.revokeUrl) {
        try { URL.revokeObjectURL(found.revokeUrl); } catch {}
      }
      return prev.filter((t) => t.id !== id);
    });
  }, []);

  // Load dashboard data
  useEffect(() => {
    api.get('auth/me/').then(res => setUser(res.data)).catch(() => {});
    api.get('transactions/').then(res => setTransactions(res.data)).catch(() => {});
    api.get('core/currencies/')
      .then(res => {
        const list = Array.isArray(res.data) ? res.data : (res.data.results || []);
        setCurrencyOptions(list);
        if (list.length && !list.find(c => c.code === currency)) setCurrency(list[0].code);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    const load = async () => {
      try {
        const [m, t, b] = await Promise.all([
          api.get('analytics/summary/month/', { params: { currency } }),
          api.get('analytics/summary/top-categories/', { params: { currency } }),
          api.get('analytics/budgets/summary/', { params: { currency } }),
        ]);
        setMonthlyData(m.data || []);
        setTopCategories(t.data || []);
        setBudgetsData(b.data || []);
      } catch {
        pushToast({ type: 'error', title: 'Analytics Error', message: 'Failed to load analytics data.' });
      }
    };
    load();
  }, [currency, pushToast]);

  // --- Logout handler ---
  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    navigate('/login');
  };

  // --- CSV Import / Export ---
  const handleImport = async () => {
    if (!csvFile) return pushToast({ type: 'error', title: 'No file selected', message: 'Choose a CSV file first.' });
    setBusy(true);
    try {
      const fd = new FormData();
      fd.append('file', csvFile);
      const res = await api.post('/transactions/import/', fd);
      const { created = 0, errors = 0, line_errors = [] } = res.data || {};
      let msg = `Created: ${created}\nErrors: ${errors}`;
      if (errors && line_errors.length) {
        const sample = line_errors.slice(0, 5).map(e => `• line ${e.line}: ${e.error}`).join('\n');
        msg += `\n\nDetails (first ${Math.min(5, line_errors.length)}):\n${sample}`;
        const csv = 'line,error\n' + line_errors.map(e => `${e.line},"${e.error}"`).join('\n');
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        pushToast({
          type: 'error',
          title: 'Import Completed with Errors',
          message: msg,
          actionLabel: 'Download errors.csv',
          onAction: () => {
            const a = document.createElement('a');
            a.href = url;
            a.download = 'import-errors.csv';
            a.click();
          },
          revokeUrl: url,
        });
      } else {
        pushToast({ type: 'success', title: 'Import Successful', message: msg });
      }
      if (created > 0) api.get('transactions/').then(r => setTransactions(r.data)).catch(() => {});
      setCsvFile(null);
    } catch (e) {
      pushToast({ type: 'error', title: 'Import Failed', message: 'CSV import failed. Check format.' });
    } finally {
      setBusy(false);
    }
  };

  const handleExport = async () => {
    setBusy(true);
    try {
      const res = await api.get('/transactions/export/');
      const filename = res.data?.filename || 'transactions.csv';
      const blob = new Blob([res.data?.content || ''], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      link.click();
      pushToast({ type: 'success', title: 'Export Ready', message: `Downloaded ${filename}` });
    } catch {
      pushToast({ type: 'error', title: 'Export Failed', message: 'Could not export CSV.' });
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="p-4 space-y-8">
      {/* Toasts */}
      <div className="fixed top-4 right-4 z-50 pointer-events-none">
        {toasts.map(t => <Toast key={t.id} {...t} onClose={closeToast} />)}
      </div>

      {/* Header */}
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="flex items-center gap-3">
          <CurrencySelector value={currency} options={currencyOptions} onChange={setCurrency} />
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow transition"
          >
            Logout
          </button>
        </div>
      </div>

      {user && <p className="text-lg">Welcome, <strong>{user.username}</strong> 👋</p>}

      {/* CSV Controls */}
      <div className="bg-white shadow p-4 rounded flex flex-wrap items-center gap-3">
        <input type="file" accept=".csv" onChange={e => setCsvFile(e.target.files[0])} className="border p-2 rounded" />
        <button
          onClick={handleImport}
          disabled={busy}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg shadow transition disabled:opacity-60"
        >
          {busy ? 'Importing…' : 'Import CSV'}
        </button>
        <button
          onClick={handleExport}
          disabled={busy}
          className="bg-gray-800 hover:bg-gray-900 text-white px-4 py-2 rounded-lg shadow transition disabled:opacity-60"
        >
          {busy ? 'Preparing…' : 'Export CSV'}
        </button>
      </div>

      <BudgetProgress items={budgetsData} colorsByCategory={colorByCategory} />

      <section>
        <h2 className="text-xl font-semibold mb-2">Monthly Summary <span className="ml-2 text-xs px-2 py-1 rounded bg-gray-100 border">{currency}</span></h2>
        <div className="h-64 bg-white shadow p-4 rounded">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={monthlyData}>
              <XAxis dataKey="month" />
              <YAxis tickFormatter={(v) => (currency === 'RSD' ? Number(v).toFixed(0) : fmt2(v))} />
              <Tooltip formatter={(value) => fmt2(value)} />
              <Bar dataKey="total" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Top Spending Categories <span className="ml-2 text-xs px-2 py-1 rounded bg-gray-100 border">{currency}</span></h2>
        <div className="h-64 bg-white shadow p-4 rounded">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={topCategories} dataKey="total" nameKey="category" outerRadius={80} label>
                {topCategories.map((entry, i) => (
                  <Cell key={i} fill={colorByCategory[entry.category] || DEFAULT_GRAY} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </section>
      {/* Management Dashboard */}
      <section className='grid grid-cols-1 lg:grid-cols-3 gap-4 mt-6'>
        <div className='lg:col-span-1 space-y-4'>
          <BalanceWidget />
          <CategoryManager />
        </div>
        <div className='lg:col-span-2 space-y-4'>
          <TransactionForm />
          <RecordsTable />
        </div>
      </section>
    </div>
  );
}
