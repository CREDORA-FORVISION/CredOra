import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import api from "../api/client";
import NavBar from "../components/NavBar";

export default function LoginPage() {
  const { role } = useParams(); // "user" or "banker"
  const navigate = useNavigate();

  const normalizedRole = role === "banker" ? "banker" : "user";

  const [form, setForm] = useState({
    usernameOrEmail: "",
    password: "",
    role: normalizedRole,
  });

  const [error, setError] = useState("");

  useEffect(() => {
    setForm((prev) => ({ ...prev, role: normalizedRole }));
  }, [normalizedRole]);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const payload = {
        username: form.usernameOrEmail,
        password: form.password,
        role: form.role,
      };

      const res = await api.post("/auth/login", payload);

      localStorage.setItem("credora_token", res.data.token);
      localStorage.setItem("credora_role", res.data.role);
      localStorage.setItem("credora_username", res.data.username);
      if (res.data.bank_code) {
        localStorage.setItem("credora_bank_code", res.data.bank_code);
      }

      if (res.data.role === "banker") {
        navigate("/bank-dashboard");
      } else {
        navigate("/user-dashboard");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid credentials.");
    }
  };

  const title =
    normalizedRole === "banker" ? "Login as Banker" : "Login to CredOra";

  const subtitle =
    normalizedRole === "banker"
      ? "Use your banker credentials issued by your bank admin."
      : "Use your registered username or email to continue.";

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <NavBar />

      <div className="flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-md">
          <div className="mb-6 text-left">
            <h1 className="text-2xl font-semibold">{title}</h1>
            <p className="text-slate-400 text-xs mt-1">{subtitle}</p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl"
          >
            {error && (
              <p className="text-xs text-red-400 mb-3 bg-red-900/30 border border-red-900 px-3 py-2 rounded">
                {error}
              </p>
            )}

            <label className="block text-xs mb-1">
              Username or Email
            </label>
            <input
              name="usernameOrEmail"
              onChange={handleChange}
              className="w-full mb-4 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />

            <label className="block text-xs mb-1">Password</label>
            <input
              type="password"
              name="password"
              onChange={handleChange}
              className="w-full mb-5 px-3 py-2 rounded-lg bg-slate-800 text-sm border border-slate-700 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />

            <button
              type="submit"
              className="w-full py-2 rounded-lg bg-emerald-500 text-black font-semibold hover:bg-emerald-400"
            >
              Login
            </button>

            <div className="mt-4 text-[11px] text-slate-400 flex flex-col gap-1">
              {normalizedRole === "banker" && (
                <span>
                  New banker?{" "}
                  <Link
                    to="/register/banker"
                    className="text-emerald-400 hover:underline"
                  >
                    Request access
                  </Link>
                  .
                </span>
              )}
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
              <span
                className="cursor-pointer hover:text-slate-200"
                onClick={() =>
                  navigate(
                    normalizedRole === "banker"
                      ? "/login/user"
                      : "/login/banker"
                  )
                }
              >
                Switch to{" "}
                {normalizedRole === "banker" ? "User Login" : "Banker Login"}
              </span>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
