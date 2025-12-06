import { useEffect, useState } from "react";
import api from "../../api/client";

export default function PastReports() {
  const [reports, setReports] = useState([]);
  const username = localStorage.getItem("credora_username");

  useEffect(() => {
    api.get(`/reports/user/${username}`).then((res) => {
      setReports(res.data.reports || []);
    });
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-700 p-5 rounded-xl">
      <h2 className="text-xl font-semibold mb-3">Past Reports</h2>

      {reports.length === 0 ? (
        <p className="text-slate-400">No previous reports found.</p>
      ) : (
        <div className="space-y-3">
          {reports.map((r) => (
            <div key={r.id} className="border border-slate-700 rounded-lg p-3">
              <p className="font-semibold">{r.input_source.toUpperCase()}</p>
              <p className="text-xs text-slate-400">
                Score: {r.overall_risk_score?.toFixed(2)}
              </p>
              <p className="text-xs text-slate-500">
                {new Date(r.created_at).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
