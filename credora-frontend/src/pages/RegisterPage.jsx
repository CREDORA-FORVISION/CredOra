// src/pages/RegisterPage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "banker",
    bank_code: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await api.post("/auth/register", form);

      localStorage.setItem("credora_token", res.data.token);
      localStorage.setItem("credora_role", res.data.role);
      localStorage.setItem("credora_username", res.data.username);
      if (res.data.bank_code) {
        localStorage.setItem("credora_bank_code", res.data.bank_code);
      }

      navigate("/bank/dashboard");
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4 text-white">
      <form
        onSubmit={handleSubmit}
        className="bg-slate-900 p-6 rounded-xl border border-slate-800 w-full max-w-sm"
      >
        <p className="text-xs text-emerald-400 mb-1">Bank Employee Onboarding</p>
        <h2 className="text-xl font-semibold mb-4">Register as Banker</h2>

        {error && (
          <p className="text-xs text-red-400 bg-red-900/30 border border-red-900 px-3 py-2 rounded mb-3">
            {error}
          </p>
        )}

        <label className="text-xs">Username</label>
        <input
          name="username"
          value={form.username}
          onChange={handleChange}
          className="w-full bg-slate-800 text-sm px-3 py-2 rounded mb-3"
        />

        <label className="text-xs">Email</label>
        <input
          name="email"
          value={form.email}
          onChange={handleChange}
          className="w-full bg-slate-800 text-sm px-3 py-2 rounded mb-3"
        />

        <label className="text-xs">Password</label>
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          className="w-full bg-slate-800 text-sm px-3 py-2 rounded mb-3"
        />

        <label className="text-xs">Bank Code</label>
        <input
          name="bank_code"
          value={form.bank_code}
          onChange={handleChange}
          placeholder="Enter bank code issued by your admin"
          className="w-full bg-slate-800 text-sm px-3 py-2 rounded mb-4"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-500 text-black py-2 rounded-lg font-semibold disabled:opacity-60"
        >
          {loading ? "Creating account..." : "Register"}
        </button>
      </form>
    </div>
  );
}
