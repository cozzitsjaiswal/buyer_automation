import { useEffect, useState } from 'react';
import { api } from '../api';

/**
 * Render the Dashboard page displaying buyer metrics and a list of recent buyers.
 *
 * Fetches data from the `/dashboard` endpoint on mount and populates local state with
 * `total_buyers`, `status_cards`, and `latest_buyers`. The UI shows a total buyers card,
 * a grid of status cards (each with a status label and count), and a table of the latest buyers.
 * Missing buyer emails are displayed as `-`.
 *
 * @returns {JSX.Element} The dashboard page element containing metrics and the latest buyers table.
 */
export default function DashboardPage() {
  const [data, setData] = useState({ total_buyers: 0, status_cards: [], latest_buyers: [] });

  useEffect(() => {
    api.get('/dashboard').then((res) => setData(res.data));
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-slate-800">Dashboard</h2>

      <div className="bg-white rounded-lg shadow p-5">
        <p className="text-slate-500">Total Buyers</p>
        <p className="text-3xl font-bold text-emerald-600">{data.total_buyers}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {data.status_cards.map((card) => (
          <div key={card.status} className="bg-white rounded-lg shadow p-4">
            <p className="text-slate-500">{card.status}</p>
            <p className="text-xl font-semibold">{card.count}</p>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow p-5 overflow-x-auto">
        <h3 className="font-semibold mb-3">Latest 10 Buyers</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="py-2">Company</th>
              <th>Country</th>
              <th>Status</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {data.latest_buyers.map((buyer) => (
              <tr key={buyer.id} className="border-b">
                <td className="py-2">{buyer.company_name}</td>
                <td>{buyer.country}</td>
                <td>{buyer.status}</td>
                <td>{buyer.email || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}