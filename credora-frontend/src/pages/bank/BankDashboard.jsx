import { useState } from "react";
import NavBar from "../../components/NavBar";
import SearchCustomers from "./SearchCustomers";
import CurrentEvaluation from "./CurrentEvaluation";
import ManualScenario from "./ManualScenario";
import UploadCSV from "./UploadCSV";
import PastReports from "./PastReports";

export default function BankerDashboard() {
  const [activeTab, setActiveTab] = useState("search");

  const tabs = [
    { key: "search", title: "Search Customers", desc: "Find & select profiles" },
    { key: "current", title: "Current Evaluation", desc: "Latest risk snapshot" },
    { key: "manual", title: "Manual Scenario", desc: "Run what-if analysis" },
    { key: "upload", title: "Upload CSV", desc: "Ingest bank statement" },
    { key: "history", title: "Past Reports", desc: "Track previous decisions" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <NavBar />

      {/* Top Tabs */}
      <div className="max-w-6xl mx-auto mt-6 px-6 flex gap-3 overflow-x-auto pb-4">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-5 py-3 rounded-xl text-sm font-semibold border
              ${
                activeTab === tab.key
                  ? "bg-emerald-500 text-black border-emerald-400"
                  : "bg-slate-900 border-slate-700 hover:bg-slate-800"
              }`}
          >
            {tab.title}
            <div className="text-[10px] text-slate-400">{tab.desc}</div>
          </button>
        ))}
      </div>

      {/* Page Title */}
      <div className="max-w-6xl mx-auto px-6 mt-4">
        <h1 className="text-3xl font-bold">Banker Dashboard</h1>
        <p className="text-xs text-slate-400 mt-1">
          Search customers, run AI risk analysis and review historic decisions.
        </p>
      </div>

      {/* Active Section */}
      <div className="max-w-6xl mx-auto px-6 mt-6">
        {activeTab === "search" && <SearchCustomers />}
        {activeTab === "current" && <CurrentEvaluation />}
        {activeTab === "manual" && <ManualScenario />}
        {activeTab === "upload" && <UploadCSV />}
        {activeTab === "history" && <PastReports />}
      </div>
    </div>
  );
}
