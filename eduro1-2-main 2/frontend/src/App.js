import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Dashboard from './Dashboard';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userType, setUserType] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const type = localStorage.getItem('user_type');
    if (token && type) {
      setIsAuthenticated(true);
      setUserType(type.toLowerCase());
    }
  }, []);

  const handleLogin = (type) => {
    setIsAuthenticated(true);
    setUserType(type.toLowerCase());
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserType(null);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/admin" />} />

        <Route path="/admin" element={
          isAuthenticated && userType === 'admin' ?
            <Dashboard userType="admin" onLogout={handleLogout} /> :
            <Login userType="admin" onLogin={handleLogin} />
        } />

        <Route path="/teacher" element={
          isAuthenticated && userType === 'teacher' ?
            <Dashboard userType="teacher" onLogout={handleLogout} /> :
            <Login userType="teacher" onLogin={handleLogin} />
        } />

        <Route path="/student" element={
          isAuthenticated && userType === 'student' ?
            <Dashboard userType="student" onLogout={handleLogout} /> :
            <Login userType="student" onLogin={handleLogin} />
        } />
      </Routes>
    </Router>
  );
}

export default App;
