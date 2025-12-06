// src/components/RiskResultCard.jsx
export default function RiskResultCard({ result }) {
  if (!result) return null;

  const { emi_stress, stability, hidden_debt, overall_risk } = result;
  const components = overall_risk?.components || {};

  return (
    <div className="mt-6 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
      <h2 className="text-xl font-semibold mb-4 text-white">
        Risk Analysis Overview
      </h2>

      <div className="grid md:grid-cols-2 gap-5">
        {/* EMI STRESS */}
        <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 shadow">
          <h3 className="font-semibold text-emerald-400 text-sm">EMI Stress</h3>
          <p className="text-slate-300 text-sm mt-1 font-bold">
            {emi_stress.emi_stress_label}
          </p>
          <p className="text-slate-500 text-xs mt-2">
            Low: {(emi_stress.probability_low * 100).toFixed(1)}% ·
            Medium: {(emi_stress.probability_medium * 100).toFixed(1)}% ·
            High: {(emi_stress.probability_high * 100).toFixed(1)}%
          </p>
          {components.emi_risk_component != null && (
            <p className="text-[11px] text-slate-500 mt-1">
              EMI risk contribution:{" "}
              {(components.emi_risk_component * 100).toFixed(1)}%
            </p>
          )}
        </div>

        {/* STABILITY */}
        <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 shadow">
          <h3 className="font-semibold text-blue-400 text-sm">
            Financial Stability
          </h3>
          <p className="text-slate-300 text-sm mt-1">
            {Math.round(stability.financial_stability_probability * 100)}%
            &nbsp;Stable
          </p>
          <p className="text-slate-500 text-xs mt-2">
            Status:{" "}
            {stability.is_financially_stable ? "Looks stable" : "Potentially unstable"}
          </p>
          {components.stability_risk_component != null && (
            <p className="text-[11px] text-slate-500 mt-1">
              Stability risk contribution:{" "}
              {(components.stability_risk_component * 100).toFixed(1)}%
            </p>
          )}
        </div>

        {/* HIDDEN DEBT */}
        <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 shadow">
          <h3 className="font-semibold text-yellow-400 text-sm">Hidden Debt</h3>
          <p className="text-slate-300 text-sm mt-1">
            {Math.round(hidden_debt.hidden_debt_risk_probability * 100)}%
            &nbsp;probability of hidden debt
          </p>
          <p className="text-slate-500 text-xs mt-2">
            Flag: {hidden_debt.high_hidden_debt_risk ? "High risk" : "Low / Moderate"}
          </p>
          {components.hidden_debt_component != null && (
            <p className="text-[11px] text-slate-500 mt-1">
              Hidden debt risk contribution:{" "}
              {(components.hidden_debt_component * 100).toFixed(1)}%
            </p>
          )}
        </div>

        {/* OVERALL RISK */}
        <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 shadow">
          <h3 className="font-semibold text-red-400 text-sm">Overall Risk</h3>
          <p className="text-slate-300 text-sm mt-1">
            Score: {overall_risk.overall_risk_score.toFixed(2)}
          </p>
          <p className="text-slate-400 text-xs mt-2">
            Bucket: <span className="font-bold">{overall_risk.risk_bucket}</span>
          </p>
        </div>
      </div>

      {/* RECOMMENDATION */}
      <div className="mt-6 bg-slate-950 p-4 border border-slate-800 rounded-xl">
        <h3 className="font-semibold text-purple-400 text-sm">Recommendation</h3>
        <p className="text-slate-300 text-xs mt-2 leading-relaxed">
          {overall_risk.recommendation}
        </p>
      </div>
    </div>
  );
}
