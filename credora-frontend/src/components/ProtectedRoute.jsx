// src/components/ProtectedRoute.jsx
import { Navigate } from "react-router-dom";

export function ProtectedUser({ children }) {
  const token = localStorage.getItem("credora_token");
  const role = localStorage.getItem("credora_role");

  if (!token) return <Navigate to="/login" replace />;
  if (role !== "user") return <Navigate to="/login" replace />;

  return children;
}

export function ProtectedBanker({ children }) {
  const token = localStorage.getItem("credora_token");
  const role = localStorage.getItem("credora_role");
  const bankCode = localStorage.getItem("credora_bank_code");

  if (!token) return <Navigate to="/login" />;
  if (role !== "banker") return <Navigate to="/login" />;
  if (!bankCode) return <Navigate to="/register-bank" />;

  return children;
}

