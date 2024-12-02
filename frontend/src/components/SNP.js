import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

function SetNewPassword() {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const username = params.get('username');
    const email = params.get('email');
    const token = params.get('token');
    if (!username || !email || !token) {
      setMessage('Invalid reset link');
      setTimeout(() => navigate('/'), 2000);
    }
  }, [location, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMessage('Passwords do not match.');
      return;
    }

    const params = new URLSearchParams(location.search);
    const username = params.get('username');
    const email = params.get('email');
    const token = params.get('token');
    try {
      const response = await axios.post('http://localhost:8000/set-new-password',
        new URLSearchParams({ username, email, password, token }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      setMessage(response.data.status);
      setTimeout(() => navigate('/login'), 2000);
    } catch (error) {
      setMessage('Failed to set password: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  return (
    <div className="form-box">
      <h2>Set New Password</h2>
      <p>Hello, {new URLSearchParams(location.search).get('username')}! Please set your new password.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="New Password"
          required
        />
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
          required
        />
        <button type="submit" className='buttonform'>Set Password</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default SetNewPassword;
