import { useNavigate } from "react-router-dom";

export default function NavBar() {
  const navigate = useNavigate();
  const role = localStorage.getItem("credora_role");

  const handleLogout = () => {
    localStorage.removeItem("credora_token");
    localStorage.removeItem("credora_role");
    navigate("/login");
  };

  return (
    <nav className="w-full bg-slate-900 border-b border-slate-800 px-4 py-3 flex justify-between">
      <h1 className="text-emerald-400 font-bold text-lg">CredOra</h1>

      <div className="flex items-center gap-4 text-sm">
        {role === "user" && (
          <button
            onClick={() => navigate("/user-dashboard")}
            className="text-slate-300 hover:text-white"
          >
            My Risk Score
          </button>
        )}

        {role === "banker" && (
          <button
            onClick={() => navigate("/bank-dashboard")}
            className="text-slate-300 hover:text-white"
          >
            Evaluate Customer
          </button>
        )}

        <button
          onClick={handleLogout}
          className="text-red-400 hover:text-red-300"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
