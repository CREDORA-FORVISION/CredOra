import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children, role }) {
  const token = localStorage.getItem("credora_token");
  const userRole = localStorage.getItem("credora_role");

  if (!token) return <Navigate to="/login" />;

  if (role && userRole !== role) return <Navigate to="/login" />;

  return children;
}
