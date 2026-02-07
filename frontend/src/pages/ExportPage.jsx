export default function ExportPage() {
  const handleExport = () => {
    window.open('http://127.0.0.1:8000/export', '_blank');
  };

  return (
    <div className="bg-white rounded-lg shadow p-8 max-w-xl">
      <h2 className="text-2xl font-semibold text-slate-800 mb-4">Export to Excel</h2>
      <p className="text-slate-600 mb-6">
        Download all buyer records with full fields as an Excel workbook.
      </p>
      <button onClick={handleExport} className="bg-emerald-600 text-white px-5 py-3 rounded-md">
        Download EU_Turmeric_Buyers.xlsx
      </button>
    </div>
  );
}
