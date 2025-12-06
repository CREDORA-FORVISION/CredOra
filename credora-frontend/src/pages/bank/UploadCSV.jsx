export default function UploadCSV() {
  return (
    <div className="p-4 bg-slate-900 rounded-xl border border-slate-700">
      <h2 className="text-lg font-semibold mb-3">Upload CSV</h2>

      <input type="file" className="text-sm" accept=".csv" />
      <button className="ml-3 px-4 py-2 bg-blue-500 text-black rounded-lg">
        Upload
      </button>
    </div>
  );
}
