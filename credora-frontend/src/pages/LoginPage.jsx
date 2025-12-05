import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

export default function LoginPage() {
  const navigate = useNavigate();
  const [role, setRole] = useState("user");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await api.post("/auth/login", {
        email,
        password,
        role,
      });

      localStorage.setItem("credora_token", res.data.token);
      localStorage.setItem("credora_role", role);

      // redirect
      if (role === "banker") {
        navigate("/bank-dashboard");
      } else {
        navigate("/user-dashboard");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-200">
      <form
        onSubmit={handleLogin}
        className="p-6 bg-slate-900 rounded-xl border border-slate-800 w-80"
      >
        <h2 className="text-lg font-semibold mb-4 text-center">
          CredOra Login
        </h2>

        {error && (
          <p className="text-red-400 text-xs bg-red-950/40 border border-red-900 p-2 rounded mb-3">
            {error}
          </p>
        )}

        <div className="mb-3">
          <label className="text-xs">Email</label>
          <input
            type="email"
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-xs"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="text-xs">Password</label>
          <input
            type="password"
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-xs"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="text-xs block mb-1">Login As</label>
          <div className="flex gap-3">
            <label className="flex items-center gap-1 text-xs">
              <input
                type="radio"
                name="role"
                value="user"
                checked={role === "user"}
                onChange={() => setRole("user")}
              />
              User
            </label>

            <label className="flex items-center gap-1 text-xs">
              <input
                type="radio"
                name="role"
                value="banker"
                checked={role === "banker"}
                onChange={() => setRole("banker")}
              />
              Banker
            </label>
          </div>
        </div>

        <button
          type="submit"
          className="w-full bg-emerald-500 text-slate-900 font-semibold text-sm py-2 rounded hover:bg-emerald-400"
        >
          Login
        </button>
      </form>
    </div>
  );
}
