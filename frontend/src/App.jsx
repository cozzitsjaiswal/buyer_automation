import { useMemo, useState } from 'react';
import Sidebar from './components/Sidebar';
import AddBuyerPage from './pages/AddBuyerPage';
import BuyerListPage from './pages/BuyerListPage';
import DashboardPage from './pages/DashboardPage';
import ExportPage from './pages/ExportPage';
import ImportUrlsPage from './pages/ImportUrlsPage';

/**
 * Root application component that manages page navigation and renders the sidebar and selected page.
 *
 * Renders a Sidebar with the current active page and a main content area showing one of:
 * Dashboard, Add Buyer, Buyer List, Import URLs, or Export to Excel.
 * @returns {JSX.Element} The app layout containing the Sidebar and the currently selected page.
 */
export default function App() {
  const [activePage, setActivePage] = useState('Dashboard');

  const page = useMemo(() => {
    switch (activePage) {
      case 'Add Buyer':
        return <AddBuyerPage />;
      case 'Buyer List':
        return <BuyerListPage />;
      case 'Import URLs':
        return <ImportUrlsPage />;
      case 'Export to Excel':
        return <ExportPage />;
      case 'Dashboard':
      default:
        return <DashboardPage />;
    }
  }, [activePage]);

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar active={activePage} onChange={setActivePage} />
      <main className="flex-1 p-6">{page}</main>
    </div>
  );
}