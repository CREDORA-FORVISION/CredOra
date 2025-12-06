import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterBank from "./pages/RegisterBank.jsx";

// USER PAGES
import UserDashboard from "./pages/user/UserDashboard.jsx";
import UserOverview from "./pages/user/UserOverview.jsx";
import UserManualScenario from "./pages/user/ManualScenario.jsx";
import UserPastReports from "./pages/user/PastReports.jsx";
import UserUploadCSV from "./pages/user/UploadCSV.jsx";

// BANK PAGES
import BankDashboard from "./pages/bank/BankDashboard.jsx";
import BankCustomerPage from "./pages/bank/BankCustomerPage.jsx";
import BankEvaluate from "./pages/bank/BankEvaluate.jsx";
import SearchCustomers from "./pages/bank/SearchCustomers.jsx";
import CurrentEvaluation from "./pages/bank/CurrentEvaluation.jsx";
import ManualScenario from "./pages/bank/ManualScenario.jsx";
import UploadCSV from "./pages/bank/UploadCSV.jsx";
import PastReports from "./pages/bank/PastReports.jsx";

import { ProtectedUser, ProtectedBanker } from "./components/ProtectedRoute.jsx";

export default function App() {
  return (
    <Routes>

      <Route path="/" element={<Home />} />
      <Route path="/login/:role" element={<LoginPage />} />
      <Route path="/register/bank" element={<RegisterBank />} />

      {/* USER ROUTES */}
      <Route element={<ProtectedUser />}>
        <Route path="/user/dashboard" element={<UserDashboard />} />
        <Route path="/user/overview" element={<UserOverview />} />
        <Route path="/user/manual" element={<UserManualScenario />} />
        <Route path="/user/reports" element={<UserPastReports />} />
        <Route path="/user/upload" element={<UserUploadCSV />} />
      </Route>

      {/* BANK ROUTES */}
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
