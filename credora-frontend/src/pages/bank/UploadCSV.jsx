import React, { useState } from "react";

export default function UploadCSV() {
  const [file, setFile] = useState(null);

  const handleUpload = () => {
    if (!file) {
      alert("Please select a CSV file first");
      return;
    }
    alert("Bank CSV uploaded successfully (mock)");
  };

  return (
    <div style={{ padding: "40px", color: "white" }}>
      <h1>Upload Customer Bank Statement (CSV)</h1>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        style={{
          padding: "6px 14px",
          background: "#7359ff",
          color: "white",
          borderRadius: "8px",
          marginLeft: "10px",
        }}
      >
        Upload
      </button>
    </div>
  );
}
