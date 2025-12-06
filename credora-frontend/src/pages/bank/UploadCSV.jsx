import React, { useState } from "react";

export default function UploadCSV() {
  const [file, setFile] = useState(null);

  // Banker CSV template (multiple customer rows)
  const handleGenerateTemplate = () => {
    const header = "customer_id,date,description,amount,balance\n";
    const blob = new Blob([header], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "bank_customer_statement_template.csv";
    link.click();
  };

  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const submitFile = async () => {
    if (!file) return alert("Please upload a CSV file!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/ml/upload-customer-statement", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      alert("Bank CSV processed!");
      console.log(data);

    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    }
  };

  return (
    <div style={{ padding: "30px", color: "white" }}>
      <h1>Bank CSV Upload</h1>
      <p>Upload multiple customer statements.</p>

      <button onClick={handleGenerateTemplate}>
        Download Bank CSV Template
      </button>

      <br /><br />

      <input type="file" accept=".csv" onChange={handleFileUpload} />

      <br /><br />

      <button onClick={submitFile}>
        Upload CSV
      </button>
    </div>
  );
}
