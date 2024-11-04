import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('name', name);
      formData.append('password', password);

      const response = await axios.post('http://localhost:8000/login',
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
          }
        }
      );

      console.log('Login response:', response.data);


      if (response.data.message === "Login successful") {
        const token = response.data.token || response.data.access_token;
        localStorage.setItem('token', token);
        navigate('/');
      } else {
        setError('Login failed. Please try again.');
      }
    } catch (error) {
      console.error('Login error:', {
        message: error.message,
        response: error.response?.data
      });

      setError('Login failed: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <div className="form-box">
    <form onSubmit={handleSubmit} >
      <h2>Login</h2>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Username"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit" className='buttonform'>Login</button>
      <button type="button" onClick={handleCancel} className='buttonform'>Cancel</button>
    </form>
    </div>
  );
};

export default Login;
