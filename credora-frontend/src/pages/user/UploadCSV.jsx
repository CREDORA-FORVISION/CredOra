import React, { useState } from "react";

export default function UserUploadCSV() {
  const [file, setFile] = useState(null);

  // Create blank CSV template for user bank statements
  const handleGenerateTemplate = () => {
    const header = "date,description,amount,balance\n";
    const blob = new Blob([header], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "user_bank_statement_template.csv";
    link.click();
  };

  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const submitFile = async () => {
    if (!file) return alert("Please upload a CSV file first!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/ml/upload-statement", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      alert("CSV processed successfully!");
      console.log(data);

    } catch (err) {
      console.error(err);
      alert("Error uploading CSV");
    }
  };

  return (
    <div style={{ padding: "30px", color: "white" }}>
      <h1>User CSV Upload</h1>
      <p>Upload your bank statement for AI risk evaluation.</p>

      <button onClick={handleGenerateTemplate}>
        Download CSV Template
      </button>

      <br /><br />

      <input type="file" accept=".csv" onChange={handleFileUpload} />

      <br /><br />

      <button onClick={submitFile}>
        Upload & Analyze
      </button>
    </div>
  );
}
