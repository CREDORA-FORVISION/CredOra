import { useEffect, useState } from "react";
import api from "../../api/client";

export default function SearchCustomers() {
  const [search, setSearch] = useState("");
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const res = await api.get(`/banker/users?q=${search}`);
    setUsers(res.data);
  };

  useEffect(() => {
    fetchUsers();
  }, [search]);

  return (
    <div className="p-4 bg-slate-900 rounded-xl border border-slate-700">
      <h2 className="text-lg font-semibold mb-2">Search Customers</h2>

      <input
        className="px-3 py-2 bg-slate-800 rounded-lg w-full"
        placeholder="Search by name or email"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="mt-4">
        {users.map((u) => (
          <div
            key={u.id}
            className="p-3 bg-slate-800 rounded-lg mb-2 border border-slate-700"
          >
            <p className="font-semibold">{u.username}</p>
            <p className="text-xs text-slate-400">{u.email}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
