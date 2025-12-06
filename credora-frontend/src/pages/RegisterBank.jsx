import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function RegisterBank() {
  const [bankName, setBankName] = useState("");
  const [adminEmail, setAdminEmail] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    if (!bankName || !adminEmail || !adminPassword) {
      setError("All fields are required.");
      return;
    }

    try {
      const res = await fetch("http://localhost:5000/auth/register-bank", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bank_name: bankName,
          admin_email: adminEmail,
          admin_password: adminPassword,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Bank registration failed");
        return;
      }

      alert("Bank Registered Successfully!");
      navigate("/");
    } catch (error) {
      setError("Server error. Try again.");
    }
  };

  return (
    <div style={{ padding: "50px", color: "white" }}>
      <h1>Register Your Bank</h1>

      {error && (
        <p style={{ color: "red", marginTop: "10px" }}>
          {error}
        </p>
      )}

      <div style={{ marginTop: "20px" }}>
        <label>Bank Name</label><br />
        <input
          type="text"
          value={bankName}
          onChange={(e) => setBankName(e.target.value)}
          style={{ padding: "8px", width: "300px" }}
        />
      </div>

      <div style={{ marginTop: "20px" }}>
        <label>Admin Email</label><br />
        <input
          type="email"
          value={adminEmail}
          onChange={(e) => setAdminEmail(e.target.value)}
          style={{ padding: "8px", width: "300px" }}
        />
      </div>

      <div style={{ marginTop: "20px" }}>
        <label>Admin Password</label><br />
        <input
          type="password"
          value={adminPassword}
          onChange={(e) => setAdminPassword(e.target.value)}
          style={{ padding: "8px", width: "300px" }}
        />
      </div>

      <button
        onClick={handleRegister}
        style={{
          marginTop: "20px",
          padding: "10px 25px",
          borderRadius: "8px",
          background: "#685ee6",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Register Bank
      </button>
    </div>
  );
}
