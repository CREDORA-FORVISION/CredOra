// src/pages/BankEvaluate.jsx
import { useParams } from "react-router-dom";
import BankerDashboard from "./BankDashboard";


export default function BankEvaluate() {
  const { username } = useParams();
  // We’re not yet using username, but this keeps the route valid.
  console.log("Evaluate username:", username);
  return <BankerDashboard />;
}
