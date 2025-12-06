import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import LoginPage from "./pages/LoginPage";
import RegisterBank from "./pages/RegisterBank";
import RegisterPage from "./pages/RegisterPage";

// USER PAGES
import UserDashboard from "./pages/user/UserDashboard";
import UserOverview from "./pages/user/UserOverview";
import UserManualScenario from "./pages/user/ManualScenario";
import UserPastReports from "./pages/user/PastReports";
import UserUploadCSV from "./pages/user/UploadCSV";

// BANK PAGES
import BankDashboard from "./pages/bank/BankDashboard";
import BankCustomerPage from "./pages/bank/BankCustomerPage";
import BankEvaluate from "./pages/bank/BankEvaluate";
import SearchCustomers from "./pages/bank/SearchCustomers";
import CurrentEvaluation from "./pages/bank/CurrentEvaluation";
import ManualScenario from "./pages/bank/ManualScenario";
import UploadCSV from "./pages/bank/UploadCSV";
import PastReports from "./pages/bank/PastReports";

import { ProtectedUser, ProtectedBanker } from "./components/ProtectedRoute";

export default function App() {
  console.log("APP RENDERED");
  return (
    <Routes>

      {/* Public */}
      <Route path="/" element={<Home />} />
      <Route path="/login/:role" element={<LoginPage />} />
      <Route path="/register/bank" element={<RegisterBank />} />

      {/* User Protected Routes */}
      <Route>
        <Route path="/user/dashboard" element={<UserDashboard />} />
        <Route path="/user/overview" element={<UserOverview />} />
        <Route path="/user/manual" element={<UserManualScenario />} />
        <Route path="/user/reports" element={<UserPastReports />} />
        <Route path="/user/upload" element={<UserUploadCSV />} />
      </Route>

      {/* Banker Protected Routes */}
      <Route element={<ProtectedBanker />}>
        <Route path="/bank/dashboard" element={<BankDashboard />} />
        <Route path="/bank/customer" element={<BankCustomerPage />} />
        <Route path="/bank/evaluate" element={<BankEvaluate />} />
        <Route path="/bank/search" element={<SearchCustomers />} />
        <Route path="/bank/current" element={<CurrentEvaluation />} />
        <Route path="/bank/manual" element={<ManualScenario />} />
        <Route path="/bank/upload" element={<UploadCSV />} />
        <Route path="/bank/reports" element={<PastReports />} />
      </Route>

    </Routes>
  );
}
