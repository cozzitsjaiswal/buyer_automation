import { useState } from 'react';
import { api, BUYER_TYPES, PRODUCT_OPTIONS, SOURCE_OPTIONS } from '../api';

/**
 * UI page for bulk importing website URLs with metadata and viewing the import results.
 *
 * Renders a textarea to paste one URL per line, controls to set country, city, buyer type, source,
 * and product interest, and an "Import URLs" button that sends the prepared payload to the
 * backend endpoint. Displays a results table showing each URL, whether import succeeded, and
 * either the buyer ID (on success) or the error message (on failure).
 *
 * @returns {JSX.Element} The Import URLs page component.
 */
export default function ImportUrlsPage() {
  const [urls, setUrls] = useState('');
  const [country, setCountry] = useState('Germany');
  const [city, setCity] = useState('');
  const [buyerType, setBuyerType] = useState('Importer');
  const [source, setSource] = useState('Manual');
  const [product, setProduct] = useState('Turmeric');
  const [results, setResults] = useState([]);

  const handleImport = async () => {
    const payload = {
      urls: urls.split('\n').map((u) => u.trim()).filter(Boolean),
      country,
      city: city || null,
      buyer_type: buyerType,
      source,
      product_interest: product,
    };

    const res = await api.post('/import-urls', payload);
    setResults(res.data.results || []);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold text-slate-800">Import URLs</h2>
      <div className="bg-white rounded-lg shadow p-5 space-y-3">
        <textarea
          className="w-full border rounded-md p-3 h-36"
          placeholder="Paste one website URL per line"
          value={urls}
          onChange={(e) => setUrls(e.target.value)}
        />
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          <input className="border rounded-md px-3 py-2" value={country} onChange={(e) => setCountry(e.target.value)} placeholder="Country" />
          <input className="border rounded-md px-3 py-2" value={city} onChange={(e) => setCity(e.target.value)} placeholder="City" />
          <select className="border rounded-md px-3 py-2" value={buyerType} onChange={(e) => setBuyerType(e.target.value)}>{BUYER_TYPES.map((v) => <option key={v}>{v}</option>)}</select>
          <select className="border rounded-md px-3 py-2" value={source} onChange={(e) => setSource(e.target.value)}>{SOURCE_OPTIONS.map((v) => <option key={v}>{v}</option>)}</select>
          <select className="border rounded-md px-3 py-2" value={product} onChange={(e) => setProduct(e.target.value)}>{PRODUCT_OPTIONS.map((v) => <option key={v}>{v}</option>)}</select>
        </div>
        <button onClick={handleImport} className="bg-emerald-600 text-white px-4 py-2 rounded-md">Import URLs</button>
      </div>

      <div className="bg-white rounded-lg shadow p-4 overflow-x-auto">
        <h3 className="font-semibold mb-2">Import Results</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="py-2">URL</th>
              <th>Success</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r, idx) => (
              <tr key={idx} className="border-b">
                <td className="py-2">{r.url}</td>
                <td>{r.success ? 'Yes' : 'No'}</td>
                <td>{r.success ? `Buyer ID: ${r.buyer_id}` : r.error}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}