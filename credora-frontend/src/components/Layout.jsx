// src/components/Layout.jsx
import NavBar from "./NavBar";

export default function Layout({ sidebarItems = [], children }) {
  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      <NavBar />
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="hidden md:flex w-56 border-r border-slate-800 bg-slate-950/60 flex-col px-3 py-4 gap-2">
          <p className="text-[11px] uppercase tracking-wide text-slate-500 mb-2">
            Workspace
          </p>
          {sidebarItems.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                if (item.href?.startsWith("#")) {
                  const el = document.querySelector(item.href);
                  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
                } else if (item.href) {
                  window.location.href = item.href;
                }
              }}
              className="text-left text-xs px-3 py-2 rounded-lg hover:bg-slate-900 text-slate-300"
            >
              <div className="font-medium">{item.label}</div>
              {item.subtitle && (
                <div className="text-[10px] text-slate-500">
                  {item.subtitle}
                </div>
              )}
            </button>
          ))}
        </aside>

        {/* Main content */}
        <main className="flex-1 px-4 md:px-8 py-6 bg-gradient-to-b from-slate-950 to-slate-900">
          {children}
        </main>
      </div>
    </div>
  );
}
