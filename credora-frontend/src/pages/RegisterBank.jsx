import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import NavBar from "../components/NavBar";

export default function RegisterBank() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    bank_name: "",
    bank_code: "",
    admin_email: "",
    admin_password: "",
  });

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const res = await api.post("/auth/register-bank", form);

      setMessage("Bank registered successfully. You can now create banker accounts.");
      // Optional: auto-redirect to banker registration
      setTimeout(() => navigate("/register/banker"), 1200);
    } catch (err) {
      setError(err.response?.data?.detail || "Bank registration failed.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <NavBar />

      <div className="flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-lg">
          <div className="mb-6 text-left">
            <p className="text-xs text-slate-400 uppercase tracking-wide">
              Bank Admin Onboarding
            </p>
            <h1 className="text-2xl font-semibold mt-1">
              Register Your Bank on CredOra
            </h1>
            <p className="text-slate-400 text-xs mt-2">
              Create a unique bank profile and issue secure banker access using
              a bank code.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl"
          >
            {message && (
              <p className="text-xs text-emerald-400 mb-3 bg-emerald-900/20 border border-emerald-700 px-3 py-2 rounded">
                {message}
              </p>
            )}
            {error && (
              <p className="text-xs text-red-400 mb-3 bg-red-900/30 border border-red-900 px-3 py-2 rounded">
                {error}
              </p>
            )}

            <label className="block text-xs mb-1">Bank Name</label>
            <input
              name="bank_name"
              onChange={handleChange}
              className="w-full mb-3 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <label className="block text-xs mb-1">Bank Code (unique)</label>
            <input
              name="bank_code"
              onChange={handleChange}
              placeholder="e.g. CREDORA_KANPUR01"
              className="w-full mb-4 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <p className="text-[11px] text-slate-400 mb-4">
              This code will be used by your bankers when registering.
            </p>

            <label className="block text-xs mb-1">Admin Email</label>
            <input
              name="admin_email"
              onChange={handleChange}
              className="w-full mb-3 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <label className="block text-xs mb-1">Admin Password</label>
            <input
              type="password"
              name="admin_password"
              onChange={handleChange}
              className="w-full mb-5 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <div className="flex gap-3">
              <button
                type="submit"
                className="px-5 py-2 rounded-lg bg-purple-500 text-black font-semibold hover:bg-purple-400"
              >
                Register Bank
              </button>
              <button
                type="button"
                onClick={() => navigate("/")}
                className="px-4 py-2 rounded-lg border border-slate-600 text-xs hover:bg-slate-900"
              >
                ← Back to Home
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
