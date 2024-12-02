import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function ResetPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      setMessage('Email is required');
      return;
    }
    try {
      const response = await axios.post('https://recipe.naurot.com/reset',
        new URLSearchParams({ email: email }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      setMessage(response.data.status || response.data.msg);
      alert(`Please go to ${email} to complete the password reset.`)
      navigate('/')
    } catch (error) {
      setMessage('An error occurred: ' + (error.response?.data?.message || 'Unknown error'));
    }
  };

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <div className="form-box">
      <form onSubmit={handleSubmit}>
        <h2>Reset Password</h2>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
          <button type="submit" className='buttonform'>Reset Password</button>
          <button type="button" onClick={handleCancel} className='buttonform'>Cancel</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default ResetPassword;
