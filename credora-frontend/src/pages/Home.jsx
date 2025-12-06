// src/pages/Home.jsx
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 text-white px-8 py-10">
      <header className="flex items-center justify-between mb-10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center text-slate-900 font-bold">
            C
          </div>
          <div className="leading-tight">
            <p className="text-sm font-semibold">CredOra</p>
            <p className="text-[11px] text-slate-400">
              Creditworthiness Intelligence
            </p>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => navigate("/login/banker")}
            className="px-4 py-1.5 text-sm rounded-lg border border-slate-700 hover:bg-slate-800"
          >
            Login
          </button>
          <button
            onClick={() => navigate("/register-bank")}
            className="px-4 py-1.5 text-sm rounded-lg bg-emerald-500 text-slate-900 font-semibold hover:bg-emerald-400"
          >
            Get Started
          </button>
        </div>
      </header>

      <main className="max-w-4xl">
        <p className="text-xs tracking-[0.2em] uppercase text-emerald-400 mb-3">
          AI-powered credit risk platform
        </p>
        <h1 className="text-4xl font-bold mb-4">Welcome to CredOra</h1>
        <p className="text-slate-300 mb-10 max-w-3xl">
          AI-powered creditworthiness intelligence for banks and NBFCs. Get EMI
          stress, financial stability, hidden-debt prediction, and loan
          eligibility — instantly.
        </p>

        {/* LOGIN */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-2">Login</h2>
          <p className="text-sm text-slate-400 mb-4">
            Already registered with CredOra? Continue as:
          </p>
          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => navigate("/login/user")}
              className="px-5 py-2 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-sm"
            >
              Login as User
            </button>
            <button
              onClick={() => navigate("/login/banker")}
              className="px-5 py-2 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-sm"
            >
              Login as Banker
            </button>
          </div>
        </section>

        {/* REGISTER BANKER */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-2">Register</h2>
          <p className="text-sm text-slate-400 mb-4">
            Only bank employees can register using a valid bank code.
          </p>
          <button
            onClick={() => navigate("/register/banker")}
            className="px-5 py-2 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-sm"
          >
            Register as Banker
          </button>
        </section>

        {/* REGISTER BANK */}
        <section className="mb-10">
          <h3 className="text-lg font-semibold mb-2">For Bank Admins</h3>
          <p className="text-sm text-slate-400 mb-4 max-w-3xl">
            Register your bank and issue secure access to your credit evaluation
            team. Control which employees can log in and view customer risk
            profiles.
          </p>
          <button
            onClick={() => navigate("/register-bank")}
            className="px-5 py-2 rounded-lg bg-emerald-500 text-slate-900 font-semibold hover:bg-emerald-400 text-sm"
          >
            Register a Bank
          </button>
        </section>
      </main>
    </div>
  );
}
