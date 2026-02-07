import { useEffect, useState } from 'react';
import { api, STATUS_OPTIONS } from '../api';

export default function BuyerListPage() {
  const [buyers, setBuyers] = useState([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const loadBuyers = async () => {
    const params = {};
    if (search) params.search = search;
    if (statusFilter) params.status = statusFilter;
    const res = await api.get('/buyers', { params });
    setBuyers(res.data);
  };

  useEffect(() => {
    loadBuyers();
  }, []);

  const updateField = async (id, payload) => {
    await api.patch(`/buyers/${id}`, payload);
    loadBuyers();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold text-slate-800">Buyer List</h2>
      <div className="bg-white rounded-lg shadow p-4 flex flex-wrap gap-3">
        <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by company/country" className="border rounded-md px-3 py-2" />
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="border rounded-md px-3 py-2">
          <option value="">All Status</option>
          {STATUS_OPTIONS.map((s) => <option key={s}>{s}</option>)}
        </select>
        <button onClick={loadBuyers} className="bg-slate-800 text-white px-4 py-2 rounded-md">Apply</button>
      </div>

      <div className="bg-white rounded-lg shadow p-4 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="py-2">Company</th>
              <th>Country</th>
              <th>Email</th>
              <th>Status</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            {buyers.map((buyer) => (
              <tr key={buyer.id} className="border-b align-top">
                <td className="py-2">{buyer.company_name}</td>
                <td>{buyer.country}</td>
                <td>{buyer.email || '-'}</td>
                <td>
                  <select
                    className="border rounded-md px-2 py-1"
                    value={buyer.status}
                    onChange={(e) => updateField(buyer.id, { status: e.target.value })}
                  >
                    {STATUS_OPTIONS.map((s) => <option key={s}>{s}</option>)}
                  </select>
                </td>
                <td>
                  <textarea
                    defaultValue={buyer.remarks || ''}
                    className="border rounded-md px-2 py-1 w-full"
                    rows={2}
                    onBlur={(e) => updateField(buyer.id, { remarks: e.target.value })}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
