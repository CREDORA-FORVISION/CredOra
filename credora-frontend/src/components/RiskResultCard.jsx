export default function RiskResultCard({ result }) {
  if (!result) return null;

  const { emi_stress, stability, hidden_debt, overall_risk } = result;

  return (
    <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {/* EMI STRESS */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-emerald-400 mb-1">
          EMI Stress
        </h3>
        <p className="text-lg font-bold">
          {emi_stress?.emi_stress_label || "-"}
        </p>
        <p className="text-xs text-slate-400 mt-2">
          Low: {emi_stress?.probability_low?.toFixed(2)} | Med:{" "}
          {emi_stress?.probability_medium?.toFixed(2)} | High:{" "}
          {emi_stress?.probability_high?.toFixed(2)}
        </p>
      </div>

      {/* STABILITY */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-sky-400 mb-1">
          Financial Stability
        </h3>
        <p className="text-lg font-bold">
          {stability?.is_financially_stable ? "STABLE" : "UNSTABLE"}
        </p>
        <p className="text-xs text-slate-400 mt-2">
          Probability stable:{" "}
          {stability?.financial_stability_probability?.toFixed(3)}
        </p>
      </div>

      {/* HIDDEN DEBT */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h3 className="text-sm font-semibold text-amber-400 mb-1">
          Hidden Debt Risk
        </h3>
        <p className="text-lg font-bold">
          {hidden_debt?.high_hidden_debt_risk ? "HIGH" : "CONTROLLED"}
        </p>
        <p className="text-xs text-slate-400 mt-2">
          Probability:{" "}
          {hidden_debt?.hidden_debt_risk_probability?.toFixed(3)}
        </p>
      </div>

      {/* OVERALL RISK – full width on small, 2 cols on large */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 md:col-span-2 lg:col-span-3">
        <h3 className="text-sm font-semibold text-pink-400 mb-1">
          Overall Loan Risk
        </h3>
        <p className="text-lg font-bold">
          {overall_risk?.risk_bucket || "-"}{" "}
          <span className="text-xs font-normal text-slate-400 ml-2">
            Score:{" "}
            {overall_risk?.overall_risk_score != null
              ? overall_risk.overall_risk_score.toFixed(3)
              : "-"}
          </span>
        </p>
        <p className="text-xs text-slate-300 mt-2 leading-relaxed">
          {overall_risk?.recommendation}
        </p>
        {overall_risk?.components && (
          <div className="mt-3 text-[11px] text-slate-400 grid gap-1 md:grid-cols-3">
            <div>
              EMI component:{" "}
              {overall_risk.components.emi_risk_component.toFixed(3)}
            </div>
            <div>
              Stability component:{" "}
              {overall_risk.components.stability_risk_component.toFixed(3)}
            </div>
            <div>
              Hidden-debt component:{" "}
              {overall_risk.components.hidden_debt_component.toFixed(3)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
