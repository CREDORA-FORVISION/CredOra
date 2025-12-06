// src/pages/RegisterBank.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

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
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      const res = await api.post("/auth/register-bank", form);

      setMessage("Bank registered successfully. You can now create banker logins.");
      // Optionally save bank_code for the admin
      if (res.data.bank_code) {
        localStorage.setItem("credora_bank_code", res.data.bank_code);
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Bank registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="bg-slate-900 border border-slate-800 rounded-xl p-8 w-full max-w-lg"
      >
        <p className="text-xs text-emerald-400 mb-2">Bank Admin Onboarding</p>
        <h1 className="text-2xl font-bold mb-2">Register Your Bank on CredOra</h1>
        <p className="text-sm text-slate-400 mb-6">
          Create a bank profile and issue secure banker access using a unique bank code.
        </p>

        {error && (
          <p className="text-xs text-red-400 bg-red-900/30 border border-red-900 px-3 py-2 rounded mb-3">
            {error}
          </p>
        )}
        {message && (
          <p className="text-xs text-emerald-400 bg-emerald-900/30 border border-emerald-900 px-3 py-2 rounded mb-3">
            {message}
          </p>
        )}

        <label className="text-xs">Bank Name</label>
        <input
          name="bank_name"
          value={form.bank_name}
          onChange={handleChange}
          className="w-full mb-3 px-3 py-2 bg-slate-800 rounded text-sm"
        />

        <label className="text-xs">Bank Code (unique)</label>
        <input
          name="bank_code"
          value={form.bank_code}
          onChange={handleChange}
          placeholder="e.g., CREDORA_KANPUR01"
          className="w-full mb-4 px-3 py-2 bg-slate-800 rounded text-sm"
        />

        <label className="text-xs">Admin Email</label>
        <input
          name="admin_email"
          value={form.admin_email}
          onChange={handleChange}
          className="w-full mb-3 px-3 py-2 bg-slate-800 rounded text-sm"
        />

        <label className="text-xs">Admin Password</label>
        <input
          type="password"
          name="admin_password"
          value={form.admin_password}
          onChange={handleChange}
          className="w-full mb-5 px-3 py-2 bg-slate-800 rounded text-sm"
        />

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2 bg-emerald-500 text-slate-900 rounded-lg font-semibold text-sm disabled:opacity-60"
          >
            {loading ? "Registering..." : "Register Bank"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/")}
            className="px-5 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
          >
            ← Back to Home
          </button>
        </div>
      </form>
    </div>
  );
}
