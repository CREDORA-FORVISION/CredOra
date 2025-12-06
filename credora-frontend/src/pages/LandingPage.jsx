// src/pages/LandingPage.jsx
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      {/* Top bar */}
      <header className="w-full flex items-center justify-between px-8 py-4 border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="flex items-center gap-2">
          <span className="text-emerald-400 font-bold text-xl">CredOra</span>
          <span className="text-[11px] text-slate-400">
            Creditworthiness Intelligence
          </span>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => navigate("/login?role=banker")}
            className="px-4 py-1.5 text-xs rounded-lg border border-slate-700 hover:bg-slate-800"
          >
            Login
          </button>
          <button
            onClick={() => navigate("/register-bank")}
            className="px-4 py-1.5 text-xs rounded-lg bg-emerald-500 text-slate-900 font-semibold hover:bg-emerald-400"
          >
            Get Started
          </button>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 flex flex-col items-start justify-center px-10 max-w-5xl">
        <p className="text-[11px] uppercase tracking-[0.2em] text-slate-500 mb-2">
          AI-first credit risk platform
        </p>

        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Welcome to <span className="text-emerald-400">CredOra</span>
        </h1>

        <p className="text-slate-300 text-sm md:text-base max-w-3xl mb-8">
          Built for banks, NBFCs and consumers. CredOra analyzes bank statements
          to estimate EMI stress, financial stability, hidden debt and overall
          loan eligibility — in seconds.
        </p>

        {/* LOGIN */}
        <section className="mb-8 w-full max-w-xl">
          <h2 className="text-lg font-semibold mb-1">Login</h2>
          <p className="text-xs text-slate-400 mb-3">
            Already registered with CredOra? Continue as:
          </p>
          <div className="flex gap-3 flex-wrap">
            <button
              onClick={() => navigate("/login?role=user")}
              className="px-5 py-2 rounded-lg bg-slate-900 border border-slate-700 text-sm hover:bg-slate-800"
            >
              Login as User
            </button>
            <button
              onClick={() => navigate("/login?role=banker")}
              className="px-5 py-2 rounded-lg bg-slate-900 border border-slate-700 text-sm hover:bg-slate-800"
            >
              Login as Banker
            </button>
          </div>
        </section>

        {/* REGISTER (bankers only) */}
        <section className="mb-8 w-full max-w-xl">
          <h2 className="text-lg font-semibold mb-1">Register</h2>
          <p className="text-xs text-slate-400 mb-3">
            New to CredOra? Bank employees can request secure access as bankers
            using a verified bank code.
          </p>
          <button
            onClick={() => navigate("/register?role=banker")}
            className="px-5 py-2 rounded-lg bg-emerald-500 text-slate-900 text-sm font-semibold hover:bg-emerald-400"
          >
            Register as Banker
          </button>
        </section>

        {/* BANK ADMIN SECTION */}
        <section className="w-full max-w-xl">
          <h3 className="text-xs font-semibold text-slate-400 mb-1">
            For Bank Admins
          </h3>
          <h2 className="text-lg font-semibold mb-1">
            Register your bank on CredOra
          </h2>
          <p className="text-xs text-slate-400 mb-3">
            Issue secure banker logins, control which employees can view and
            evaluate customer risk profiles, and centralize all customer reports
            under a single bank code.
          </p>

          <ul className="text-[11px] text-slate-400 mb-4 list-disc list-inside space-y-1">
            <li>Onboard once using a unique bank code</li>
            <li>Grant / revoke banker access in real time</li>
            <li>Centralized view of all customer risk reports</li>
          </ul>

          <button
            onClick={() => navigate("/register-bank")}
            className="px-5 py-2 rounded-lg bg-purple-500 text-slate-900 text-sm font-semibold hover:bg-purple-400"
          >
            Register a Bank
          </button>
        </section>
      </main>
    </div>
  );
}
