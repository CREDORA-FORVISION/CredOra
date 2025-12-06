import api from "../../api/client";
import { useState, useEffect } from "react";

export default function ManualScenario() {
  const [loading, setLoading] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const username = localStorage.getItem("credora_username");

  useEffect(() => {
    api.get(`/reports/user/${username}`).then((res) => {
      setUserInfo(res.data.user);
    });
  }, []);

  const runManual = async () => {
    setLoading(true);

    const sample = {
      income: 50000,
      expense: 20000,
      emi_amount: 3000,
      avg_balance: 15000,
      min_balance: 2000,
      num_transactions: 50,
      num_emi_txns: 2,
      customer_age: 28,
      income_volatility: 0.13,
      wallet_credit_usage: 5000,
      freq_new_credit: 1,
      bnpl_txn_count: 2,
      microloan_txn_count: 1,
      bnpl_spend: 1000,
      microloan_spend: 1500,
      hidden_emi_amount: 3500,
      high_risk_merchants: 1,
    };

    const ml = await api.post("/ml/predict", sample);

    await api.post("/reports/save", {
      user_id: userInfo.id,
      input_source: "manual",
      result: ml.data,
    });

    setLoading(false);
    alert("Manual analysis completed!");
  };

  return (
    <div className="bg-slate-900 border border-slate-700 p-5 rounded-xl">
      <h2 className="text-xl font-semibold mb-2">Manual What-If Analysis</h2>

      <button
        onClick={runManual}
        disabled={loading}
        className="px-4 py-2 bg-emerald-500 text-black rounded-lg"
      >
        {loading ? "Running..." : "Run Analysis"}
      </button>
    </div>
  );
}
