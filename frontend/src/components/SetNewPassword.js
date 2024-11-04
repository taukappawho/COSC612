import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

function SetNewPassword() {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get('token');
    if (!token) {
      setMessage('Invalid or expired link');
      setTimeout(() => navigate('/'), 2000);
    } else {
      try {
        const decoded = jwtDecode(token);
        setUsername(decoded.name);
      } catch (error) {
        console.error('Error decoding token:', error);
      }
    }
  }, [location, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password.length < 8) {
      setMessage('Password must be at least 8 characters');
      return;
    }

    if (password !== confirmPassword) {
      setMessage('Passwords do not match');
      return;
    }

    const params = new URLSearchParams(location.search);
    const token = params.get('token');

    try {
      const formData = new URLSearchParams();
      formData.append('password', password);
      formData.append('token', token);

      const response = await axios.post('http://localhost:8000/set-password',
        formData,
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );

      setMessage(response.data.msg);
      setTimeout(() => navigate('/login'), 2000);
    } catch (error) {
      setMessage('Failed to set password: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  return (
    <div className="form-box">
      {username && <h2>Hello {username}!</h2>}
      <h3>Set Your Password</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="New Password (minimum 8 characters)"
          required
          minLength="8"
        />
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
          required
        />
        <button type="submit" className='buttonform'>Set Password</button>
        <button type="button" onClick={() => navigate('/')} className='buttonform'>Cancel</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default SetNewPassword;
