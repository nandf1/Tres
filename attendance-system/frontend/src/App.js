import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Attendance from './pages/Attendance';
import LeaveRequests from './pages/LeaveRequests';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <div className="sidebar-header">
            <h2>Attendance System</h2>
          </div>
          <ul className="nav-menu">
            <li>
              <Link to="/">
                <span className="icon">📊</span>
                Dashboard
              </Link>
            </li>
            <li>
              <Link to="/employees">
                <span className="icon">👥</span>
                Employees
              </Link>
            </li>
            <li>
              <Link to="/attendance">
                <span className="icon">✅</span>
                Attendance
              </Link>
            </li>
            <li>
              <Link to="/leave-requests">
                <span className="icon">📅</span>
                Leave Requests
              </Link>
            </li>
          </ul>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/attendance" element={<Attendance />} />
            <Route path="/leave-requests" element={<LeaveRequests />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
