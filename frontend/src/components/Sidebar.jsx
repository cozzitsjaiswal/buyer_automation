const navItems = ['Dashboard', 'Add Buyer', 'Buyer List', 'Import URLs', 'Export to Excel'];

export default function Sidebar({ active, onChange }) {
  return (
    <aside className="w-64 bg-slate-900 text-white min-h-screen p-5">
      <h1 className="text-lg font-semibold mb-8">EU Buyer Automation</h1>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <button
            key={item}
            onClick={() => onChange(item)}
            className={`w-full text-left px-3 py-2 rounded-md transition ${
              active === item ? 'bg-emerald-600' : 'hover:bg-slate-800'
            }`}
          >
            {item}
          </button>
        ))}
      </nav>
    </aside>
  );
}
