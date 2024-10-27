import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function CreateAccount() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !email) {
      setMessage('Username and email are required');
      return;
    }
    try {
      const response = await axios.post('http://localhost:8000/create',
        new URLSearchParams({ name: username, email: email }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      console.log('Response:', response.data);
      setMessage(response.data.status || response.data.msg);
      if (response.data.status) {
        setTimeout(() => navigate('/'), 3000);
      }
    } catch (error) {
      console.error('Error object:', error);
      console.error('Error response:', error.response);
      setMessage('An error occurred: ' + (error.response?.data?.message || error.message || 'Unknown error'));
    }
  };

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <div className="form-box">
      <form onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
          <button type="submit" className='buttonform'>Create Account</button>
          <button type="button" onClick={handleCancel} className='buttonform'>Cancel</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default CreateAccount;
