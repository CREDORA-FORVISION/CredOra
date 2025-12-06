import { useState } from "react";
import NavBar from "../../components/NavBar";
import UserOverview from "./UserOverview";
import UploadCSV from "./UploadCSV";
import ManualScenario from "./ManualScenario";
import PastReports from "./PastReports";

export default function UserDashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const username = localStorage.getItem("credora_username");

  const tabs = [
    { key: "overview", title: "My Overview", desc: "Latest evaluation" },
    { key: "upload", title: "Upload CSV", desc: "Add bank statements" },
    { key: "manual", title: "Manual Scenario", desc: "Run manual analysis" },
    { key: "history", title: "Past Reports", desc: "View score history" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <NavBar />

      {/* Tabs */}
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

      {/* Header */}
      <div className="max-w-6xl mx-auto px-6 mt-4">
        <h1 className="text-3xl font-bold">User Dashboard</h1>
        <p className="text-xs text-slate-400 mt-1">
          Logged in as <span className="font-semibold text-emerald-400">
            {username}
          </span>
        </p>
      </div>

      {/* Active Tab */}
      <div className="max-w-6xl mx-auto px-6 mt-6">
        {activeTab === "overview" && <UserOverview />}
        {activeTab === "upload" && <UploadCSV />}
        {activeTab === "manual" && <ManualScenario />}
        {activeTab === "history" && <PastReports />}
      </div>
    </div>
  );
}
