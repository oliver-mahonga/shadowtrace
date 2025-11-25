import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="flex bg-black text-white min-h-screen">
      
      {/* Sidebar */}
      <Sidebar />

      {/* Main content area */}
      <div className="flex-1 flex flex-col">
        <Topbar />

        {/* Page content */}
        <div className="p-8 bg-black/70 flex-1 overflow-auto">
          {children}
        </div>
      </div>
    </main>
  );
}
