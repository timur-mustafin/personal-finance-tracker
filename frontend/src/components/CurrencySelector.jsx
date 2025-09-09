import React from 'react';

export default function CurrencySelector({ value, options, onChange }) {
  return (
	<div className="flex items-center gap-2">
	  <label className="text-sm text-gray-600">Currency:</label>
	  <select
		className="border rounded px-2 py-1 text-sm"
		value={value}
		onChange={(e) => onChange(e.target.value)}
	  >
		{(options || []).map((c) => (
		  <option key={c.code} value={c.code}>
			{c.code}
		  </option>
		))}
	  </select>
	</div>
  );
}