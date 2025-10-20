
export const fmtMoney = (amount, currency = 'USD') =>
  new Intl.NumberFormat(undefined, { style: 'currency', currency, maximumFractionDigits: 2 }).format(Number(amount || 0));

export const fmt2 = (n) => Number(n).toFixed(2);
