import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import BudgetProgress from '../components/BudgetProgress';
import CurrencySelector from '../components/CurrencySelector';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#a4de6c'];

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);
  const [topCategories, setTopCategories] = useState([]);
  const [budgetsData, setBudgetsData] = useState([]);

  const [currency, setCurrency] = useState('USD');
  const [currencyOptions, setCurrencyOptions] = useState([]);

  // Initial fetch: user, transactions, currencies
  useEffect(() => {
    api.get('auth/me/').then(res => setUser(res.data)).catch(() => {});
    api.get('transactions/').then(res => setTransactions(res.data)).catch(() => {});

    api.get('core/currencies/')
      .then(res => {
        const list = Array.isArray(res.data) ? res.data : (res.data.results || []);
        setCurrencyOptions(list);
        if (list.length && !list.find(c => c.code === currency)) {
          setCurrency(list[0].code);
        }
      })
      .catch(() => {});
  }, []);

  // Re-fetch analytics when currency changes
  useEffect(() => {
    const load = async () => {
      try {
        const [m, t, b] = await Promise.all([
          api.get('analytics/summary/month/', { params: { currency } }),
          api.get('analytics/summary/top-categories/', { params: { currency } }),
          api.get('analytics/budgets/summary/', { params: { currency } }),
        ]);
        setMonthlyData(Array.isArray(m.data) ? m.data : []);
        setTopCategories(Array.isArray(t.data) ? t.data : []);
        setBudgetsData(Array.isArray(b.data) ? b.data : []);
      } catch (e) {
        console.error('Analytics fetch failed', e);
      }
    };
    load();
  }, [currency]);

  return (
    <div className="p-4 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <CurrencySelector value={currency} options={currencyOptions} onChange={setCurrency} />
      </div>

      {user && <p className="text-lg">Welcome, <strong>{user.username}</strong> 👋</p>}

      <BudgetProgress items={budgetsData} />

      <section>
        <h2 className="text-xl font-semibold mb-2">Monthly Summary</h2>
        <div className="h-64 bg-white shadow p-4 rounded">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={monthlyData}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Top Spending Categories</h2>
        <div className="h-64 bg-white shadow p-4 rounded">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={topCategories}
                dataKey="total"
                nameKey="category"
                outerRadius={80}
                label
              >
                {topCategories.map((entry, index) => (
                  <Cell key={`cell-${index}`} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}
