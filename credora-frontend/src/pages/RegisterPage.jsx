import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import api from "../api/client";
import NavBar from "../components/NavBar";

export default function RegisterPage() {
  const { role } = useParams(); // should be "banker"
  const navigate = useNavigate();
  const normalizedRole = role === "banker" ? "banker" : "user";

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    bank_code: "",
    role: "banker",
  });
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Always force banker for this page
    setForm((prev) => ({ ...prev, role: "banker" }));
  }, []);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const res = await api.post("/auth/register", form);

      localStorage.setItem("credora_token", res.data.token);
      localStorage.setItem("credora_role", res.data.role);
      localStorage.setItem("credora_username", res.data.username);
      if (res.data.bank_code) {
        localStorage.setItem("credora_bank_code", res.data.bank_code);
      }

      setMessage("Banker registered successfully.");
      setTimeout(() => navigate("/bank-dashboard"), 700);
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed.");
    }
  };

  // If someone opens /register/user, show info-only screen
  if (normalizedRole !== "banker") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <NavBar />
        <div className="max-w-xl mx-auto px-6 py-20 text-left">
          <h1 className="text-2xl font-semibold mb-2">User Accounts</h1>
          <p className="text-slate-300 text-sm mb-4">
            End-users are onboarded through their bank. You cannot create a
            direct user account on CredOra.
          </p>
          <p className="text-slate-400 text-sm mb-6">
            Please contact your bank and ask them to invite you to CredOra or
            share your login details.
          </p>
          <button
            onClick={() => navigate("/")}
            className="px-4 py-2 rounded-lg bg-emerald-500 text-black text-sm font-semibold"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  // Banker registration UI
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <NavBar />

      <div className="flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-md">
          <div className="mb-6 text-left">
            <h1 className="text-2xl font-semibold">Register as Banker</h1>
            <p className="text-slate-400 text-xs mt-1">
              Use the bank code shared by your bank admin to request secure
              access.
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

            <label className="block text-xs mb-1">Full Name / Username</label>
            <input
              name="username"
              onChange={handleChange}
              className="w-full mb-3 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <label className="block text-xs mb-1">Work Email</label>
            <input
              name="email"
              onChange={handleChange}
              className="w-full mb-3 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <label className="block text-xs mb-1">Password</label>
            <input
              type="password"
              name="password"
              onChange={handleChange}
              className="w-full mb-3 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <label className="block text-xs mb-1">Bank Code</label>
            <input
              name="bank_code"
              onChange={handleChange}
              placeholder="e.g. CREDORA_KANPUR01"
              className="w-full mb-5 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700"
            />

            <button
              type="submit"
              className="w-full py-2 rounded-lg bg-emerald-500 text-black font-semibold hover:bg-emerald-400"
            >
              Register as Banker
            </button>

            <div className="mt-4 text-[11px] text-slate-400 flex flex-col gap-1">
              <span>
                Already have access?{" "}
                <Link
                  to="/login/banker"
                  className="text-emerald-400 hover:underline"
                >
                  Login as banker
                </Link>
                .
              </span>
              <span>
                Bank admin?{" "}
                <Link
                  to="/register-bank"
                  className="text-purple-400 hover:underline"
                >
                  Register your bank
                </Link>
                .
              </span>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
