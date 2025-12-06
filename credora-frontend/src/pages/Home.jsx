import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 text-white px-8 py-16">
      {/* HEADER */}
      <motion.h1
        className="text-5xl font-bold mb-6 text-emerald-400"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Welcome to CredOra
      </motion.h1>

      <motion.p
        className="max-w-3xl text-lg text-slate-300 mb-12"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        AI-powered creditworthiness intelligence for banks and NBFCs.  
        Get EMI stress, financial stability, hidden-debt prediction, and loan eligibility — instantly.
      </motion.p>

      {/* LOGIN */}
      <div className="mb-14">
        <h2 className="text-2xl font-semibold mb-4">Login</h2>

        <div className="flex gap-4">
          <button
            onClick={() => navigate("/login/user")}
            className="px-6 py-3 bg-emerald-500 text-black rounded-xl text-lg font-semibold hover:bg-emerald-400 transition"
          >
            Login as User
          </button>

          <button
            onClick={() => navigate("/login/banker")}
            className="px-6 py-3 bg-blue-500 text-black rounded-xl text-lg font-semibold hover:bg-blue-400 transition"
          >
            Login as Banker
          </button>
        </div>
      </div>

      {/* REGISTER (ONLY BANKERS) */}
      <div className="mb-14">
        <h2 className="text-2xl font-semibold mb-4">Register</h2>

        <p className="text-slate-400 mb-3">
          Only bank employees can register using a valid bank code.
        </p>

        <button
          onClick={() => navigate("/register/banker")}
          className="px-6 py-3 bg-slate-800 border border-slate-600 rounded-xl text-lg hover:bg-slate-700 transition"
        >
          Register as Banker
        </button>
      </div>

      {/* BANK REGISTRATION */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">For Bank Admins</h2>

        <p className="text-slate-400 max-w-2xl mb-3">
          Register your bank and issue secure access to your credit evaluation team.
        </p>

        <button
          onClick={() => navigate("/register-bank")}
          className="px-6 py-3 bg-purple-600 rounded-xl text-lg font-semibold hover:bg-purple-500 transition"
        >
          Register a Bank
        </button>
      </div>
    </div>
  );
}
