import { useNavigate, useLocation } from "react-router-dom";

export default function NavBar() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("credora_token");
  const role = localStorage.getItem("credora_role");
  const username = localStorage.getItem("credora_username");

  const onLogout = () => {
    localStorage.removeItem("credora_token");
    localStorage.removeItem("credora_role");
    localStorage.removeItem("credora_username");
    localStorage.removeItem("credora_bank_code");
    navigate("/");
  };

  const onLoginClick = () => {
    // default login screen for banker; user can switch tab on Home
    navigate("/login/user");
  };

  const isHome = location.pathname === "/";

  return (
    <nav className="w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur">
      <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
        {/* Logo / Brand */}
        <button
          onClick={() => navigate("/")}
          className="flex items-baseline gap-2"
        >
          <span className="w-7 h-7 rounded-lg bg-emerald-500 flex items-center justify-center text-slate-950 font-bold text-lg">
            C
          </span>
          <div className="text-left leading-tight">
            <p className="font-semibold text-sm">CredOra</p>
            <p className="text-[10px] text-slate-400">
              Creditworthiness Intelligence
            </p>
          </div>
        </button>

        {/* Right section */}
        <div className="flex items-center gap-3 text-xs">
          {token && role && (
            <span className="hidden md:inline text-slate-400">
              {role === "banker" ? "Banker" : "User"} ·{" "}
              <span className="text-slate-200 font-medium">{username}</span>
            </span>
          )}

          {!token && isHome && (
            <>
              <button
                onClick={onLoginClick}
                className="px-3 py-1 rounded-lg border border-slate-600 hover:bg-slate-800"
              >
                Login
              </button>
              <button
                onClick={() => navigate("/register-bank")}
                className="px-3 py-1 rounded-lg bg-emerald-500 text-black font-semibold hover:bg-emerald-400"
              >
                Get Started
              </button>
            </>
          )}

          {token && (
            <button
              onClick={onLogout}
              className="px-3 py-1 rounded-lg border border-red-500 text-red-300 hover:bg-red-950/40 text-xs"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
