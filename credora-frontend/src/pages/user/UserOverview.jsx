import { useEffect, useState } from "react";
import api from "../../api/client";
import RiskResultCard from "../../components/RiskResultCard";

export default function UserOverview() {
  const [userInfo, setUserInfo] = useState(null);
  const [latestReport, setLatestReport] = useState(null);
  const username = localStorage.getItem("credora_username");

  const loadLatest = async () => {
    const res = await api.get(`/reports/user/${username}`);
    setUserInfo(res.data.user);
    setLatestReport(res.data.reports?.[0] || null);
  };

  useEffect(() => {
    if (username) loadLatest();
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-700 p-5 rounded-xl">
      <h2 className="text-xl font-semibold">My Latest Risk Score</h2>

      {latestReport ? (
        <RiskResultCard result={JSON.parse(latestReport.raw_result_json)} />
      ) : (
        <p className="text-slate-400 mt-3">
          No reports available. Upload a CSV or run manual analysis.
        </p>
      )}
    </div>
  );
}
