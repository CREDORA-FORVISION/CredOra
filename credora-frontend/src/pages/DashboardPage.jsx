import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import NavBar from "../components/NavBar";
import RiskResultCard from "../components/RiskResultCard";

export default function DashboardPage({ mode }) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("manual");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // ------------------------------------
  // MANUAL FORM STATE
  // ------------------------------------
  const [manual, setManual] = useState({
    income: 50000,
    expense: 20000,
    emi_amount: 3000,
    avg_balance: 15000,
    min_balance: 2000,
    num_transactions: 70,
    num_emi_txns: 2,
    customer_age: 28,
    income_volatility: 0.1,
    wallet_credit_usage: 5000,
    freq_new_credit: 1,
    bnpl_txn_count: 2,
    microloan_txn_count: 1,
    bnpl_spend: 1500,
    microloan_spend: 2000,
    hidden_emi_amount: 3500,
    high_risk_merchants: 3,
  });

  // ------------------------------------
  // CHECK AUTH + REDIRECT
  // ------------------------------------
  useEffect(() => {
    const token = localStorage.getItem("credora_token");
    const role = localStorage.getItem("credora_role");

    if (!token) navigate("/login");
    if (role !== mode) navigate("/login");
  }, [navigate, mode]);

  // ------------------------------------
  // HANDLE CHANGES
  // ------------------------------------
  const handleManualChange = (e) => {
    const { name, value } = e.target;
    setManual((prev) => ({ ...prev, [name]: Number(value) }));
  };

  // ------------------------------------
  // BUILD PAYLOAD EXACTLY LIKE BACKEND NEEDS
  // ------------------------------------
  const buildFeaturePayload = () => {
    const m = manual;
    const income = m.income;
    const expense = m.expense;
    const net_savings = income - expense;

    return {
      income,
      expense,
      net_savings,
      savings_rate: income > 0 ? net_savings / income : 0,
      emi_amount: m.emi_amount,
      foir: income > 0 ? m.emi_amount / income : 0,

      avg_balance: m.avg_balance,
      min_balance: m.min_balance,
      num_transactions: m.num_transactions,
      num_emi_txns: m.num_emi_txns,
      customer_age: m.customer_age,

      hidden_debt_risk:
        m.num_transactions > 0
          ? (m.bnpl_txn_count + m.microloan_txn_count) /
            m.num_transactions
          : 0,

      missed_payments: 0,
      num_credit_lines: 1,
      foir_current: income > 0 ? m.emi_amount / income : 0,
      foir_new: income > 0 ? m.emi_amount / income + 0.05 : 0,

      income_volatility: m.income_volatility,
      spending_growth: income > 0 ? expense / income : 0,

      bnpl_txn_count: m.bnpl_txn_count,
      microloan_txn_count: m.microloan_txn_count,
      bnpl_spend: m.bnpl_spend,
      microloan_spend: m.microloan_spend,

      hidden_emi_amount: m.hidden_emi_amount,
      hidden_emi_to_income_ratio:
        income > 0 ? m.hidden_emi_amount / income : 0,

      wallet_credit_usage: m.wallet_credit_usage,
      freq_new_credit: m.freq_new_credit,
      high_risk_merchants: m.high_risk_merchants,
    };
  };

  // ------------------------------------
  // SUBMIT MANUAL FORM
  // ------------------------------------
  const handleManualSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);

    try {
      const payload = buildFeaturePayload();
      const res = await api.post("/ml/predict", payload);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error occurred.");
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------
  // SUBMIT CSV (BANKER ONLY)
  // ------------------------------------
  const handleCsvSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);

    const file = document.getElementById("csvFileInput")?.files?.[0];
    if (!file) {
      setError("Please choose a CSV file first.");
      setLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/ml/predict-from-csv", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "CSV upload failed.");
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------
  // RENDER
  // ------------------------------------
  return (
    <div className="min-h-screen flex flex-col">
      <NavBar />

      <main className="flex-1 px-4 md:px-8 py-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-lg font-semibold mb-1">
            {mode === "banker"
              ? "Customer Loan Risk Evaluation"
              : "Your Personal Loan Eligibility Check"}
          </h2>

          <p className="text-xs text-slate-400 mb-4">
            {mode === "banker"
              ? "Upload customer's bank statement or enter summary values."
              : "Enter your financial summary to get your risk analysis."}
          </p>

          {/* TABS (CSV only for banker) */}
          <div className="inline-flex mb-4 rounded-full bg-slate-900 border border-slate-800 p-1">
            <button
              onClick={() => setActiveTab("manual")}
              className={`px-3 py-1 text-xs rounded-full ${
                activeTab === "manual"
                  ? "bg-emerald-500 text-slate-900"
                  : "text-slate-300"
              }`}
            >
              Manual Form
            </button>

            {mode === "banker" && (
              <button
                onClick={() => setActiveTab("csv")}
                className={`px-3 py-1 text-xs rounded-full ${
                  activeTab === "csv"
                    ? "bg-emerald-500 text-slate-900"
                    : "text-slate-300"
                }`}
              >
                Upload CSV
              </button>
            )}
          </div>

          {/* ERROR */}
          {error && (
            <p className="text-xs text-red-400 bg-red-950/40 px-3 py-2 rounded mb-3">
              {error}
            </p>
          )}

          {/* MANUAL FORM */}
          {activeTab === "manual" && (
            <form
              onSubmit={handleManualSubmit}
              className="grid gap-4 md:grid-cols-3 bg-slate-900 border border-slate-800 rounded-2xl p-4"
            >
              {/* Always visible */}
              <NumberInput label="Monthly Income" name="income" value={manual.income} onChange={handleManualChange} />
              <NumberInput label="Monthly Expense" name="expense" value={manual.expense} onChange={handleManualChange} />
              <NumberInput label="Existing EMI" name="emi_amount" value={manual.emi_amount} onChange={handleManualChange} />

              <NumberInput label="Avg Balance" name="avg_balance" value={manual.avg_balance} onChange={handleManualChange} />
              <NumberInput label="Min Balance" name="min_balance" value={manual.min_balance} onChange={handleManualChange} />
              <NumberInput label="# Total Transactions" name="num_transactions" value={manual.num_transactions} onChange={handleManualChange} />

              <NumberInput label="# EMI Transactions" name="num_emi_txns" value={manual.num_emi_txns} onChange={handleManualChange} />
              <NumberInput label="Customer Age" name="customer_age" value={manual.customer_age} onChange={handleManualChange} />

              {/* ADVANCED FIELDS — ONLY FOR BANKER */}
              {mode === "banker" && (
                <>
                  <NumberInput label="Income Volatility" name="income_volatility" step="0.01" value={manual.income_volatility} onChange={handleManualChange} />
                  <NumberInput label="Wallet Credit Usage" name="wallet_credit_usage" value={manual.wallet_credit_usage} onChange={handleManualChange} />

                  <NumberInput label="BNPL Txn Count" name="bnpl_txn_count" value={manual.bnpl_txn_count} onChange={handleManualChange} />
                  <NumberInput label="Microloan Txn Count" name="microloan_txn_count" value={manual.microloan_txn_count} onChange={handleManualChange} />

                  <NumberInput label="BNPL Spend" name="bnpl_spend" value={manual.bnpl_spend} onChange={handleManualChange} />
                  <NumberInput label="Microloan Spend" name="microloan_spend" value={manual.microloan_spend} onChange={handleManualChange} />

                  <NumberInput label="Hidden EMI Amount" name="hidden_emi_amount" value={manual.hidden_emi_amount} onChange={handleManualChange} />

                  <NumberInput label="High Risk Merchants" name="high_risk_merchants" value={manual.high_risk_merchants} onChange={handleManualChange} />
                  <NumberInput label="New Credit Frequency" name="freq_new_credit" value={manual.freq_new_credit} onChange={handleManualChange} />
                </>
              )}

              <div className="md:col-span-3 flex justify-end mt-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 text-sm rounded-xl bg-emerald-500 text-slate-900 hover:bg-emerald-400"
                >
                  {loading ? "Scoring..." : "Run Analysis"}
                </button>
              </div>
            </form>
          )}

          {/* CSV UPLOAD (only banker) */}
          {activeTab === "csv" && mode === "banker" && (
            <form
              onSubmit={handleCsvSubmit}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-4 max-w-xl"
            >
              <input id="csvFileInput" type="file" accept=".csv" className="text-xs" />
              <button className="mt-4 px-4 py-2 bg-emerald-500 text-slate-900 rounded-xl">
                {loading ? "Uploading..." : "Analyze CSV"}
              </button>
            </form>
          )}

          {/* RESULTS */}
          <RiskResultCard result={result} />
        </div>
      </main>
    </div>
  );
}

function NumberInput({ label, name, value, onChange, step = "1" }) {
  return (
    <div className="flex flex-col">
      <label className="text-xs text-slate-300 mb-1">{label}</label>
      <input
        type="number"
        step={step}
        name={name}
        value={value}
        onChange={onChange}
        className="px-2 py-1.5 rounded bg-slate-950 text-xs border border-slate-800"
      />
    </div>
  );
}
