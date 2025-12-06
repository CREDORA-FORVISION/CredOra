// src/pages/BankCustomerPage.jsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../../api/client";
import Layout from "../../components/Layout";
import RiskResultCard from "../../components/RiskResultCard";
import { bankerSidebar } from "../../sidebars/bankerSidebar";

export default function BankCustomerPage() {
  const { username } = useParams();
  const [userData, setUserData] = useState(null);
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get(`/reports/user/${username}`);
        setUserData(res.data.user);
        setReports(res.data.reports || []);
      } catch (err) {
        console.error(err);
        setError("Could not load user reports.");
      }
    };
    if (username) load();
  }, [username]);

  return (
    <Layout sidebarItems={bankerSidebar}>
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">
          Customer: {username || "Unknown"}
        </h1>

        {error && (
          <p className="text-xs text-red-400 bg-red-900/30 border border-red-900 px-3 py-2 rounded mb-3">
            {error}
          </p>
        )}

        {userData && (
          <p className="text-xs text-slate-400 mb-4">
            Email: {userData.email} · Joined:{" "}
            {new Date(userData.created_at).toLocaleDateString()}
          </p>
        )}

        {reports.length === 0 ? (
          <p className="text-slate-400 mt-4">No reports for this customer.</p>
        ) : (
          <>
            <h2 className="text-lg font-semibold mt-4 mb-2">Latest Report</h2>
            <RiskResultCard
              result={JSON.parse(reports[0].raw_result_json)}
            />

            <h2 className="text-lg font-semibold mt-6 mb-2">
              All Past Reports
            </h2>
            <ul className="space-y-2 text-xs text-slate-300">
              {reports.map((r) => (
                <li key={r.id} className="border border-slate-700 rounded p-3">
                  {r.input_source.toUpperCase()} · Score:{" "}
                  {r.overall_risk_score?.toFixed(2)} ·{" "}
                  {new Date(r.created_at).toLocaleString()}
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </Layout>
  );
}
