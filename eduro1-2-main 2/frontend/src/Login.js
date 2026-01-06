import React, { useState } from 'react';
import { login } from './api';
import './Login.css';

function Login({ userType, onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await login(userType, email, password);
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user_type', data.user_type);
      localStorage.setItem('user_data', JSON.stringify(data.user));
      onLogin(data.user_type);
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const demoCredentials = {
    admin: { email: 'admin@sims.edu', password: 'admin123' },
    teacher: { email: 'teacher@sims.edu', password: 'teacher123' },
    student: { email: 'student@sims.edu', password: 'student123' },
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>SIMS - {userType.toUpperCase()} Login</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <div className="error">{error}</div>}
          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div className="demo-info">
          <p><strong>Demo Credentials:</strong></p>
          <p>Email: {demoCredentials[userType].email}</p>
          <p>Password: {demoCredentials[userType].password}</p>
        </div>
      </div>
    </div>
  );
}

export default Login;
