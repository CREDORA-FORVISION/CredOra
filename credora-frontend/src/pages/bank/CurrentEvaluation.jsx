import RiskResultCard from "../../components/RiskResultCard";

export default function CurrentEvaluation() {
  return (
    <div className="p-4 bg-slate-900 rounded-xl border border-slate-700">
      <h2 className="text-lg font-semibold mb-3">Current Evaluation</h2>
      <p className="text-slate-400 text-sm">
        Select a customer from Search tab to view risk evaluation.
      </p>
    </div>
  );
}
