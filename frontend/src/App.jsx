import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";
import "./App.css";

// Pages
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import NotFoundPage from "./pages/NotFoundPage";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState("user"); // 'user' or 'admin'

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/login"
            element={
              <LoginPage
                setIsAuthenticated={setIsAuthenticated}
                setUserRole={setUserRole}
              />
            }
          />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/dashboard/user"
            element={
              <UserDashboard
                isAuthenticated={isAuthenticated}
                userRole={userRole}
              />
            }
          />
          <Route
            path="/dashboard/admin"
            element={
              <AdminDashboard
                isAuthenticated={isAuthenticated}
                userRole={userRole}
              />
            }
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
