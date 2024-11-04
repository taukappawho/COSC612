import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function ResetPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('email', email);

      const response = await axios.post('http://localhost:8000/reset',
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );

      setMessage(response.data.msg || 'Check your email for reset instructions');
      if (response.data.status === 200) {
        setTimeout(() => navigate('/'), 3000);
      }
    } catch (error) {
      setMessage('An error occurred: ' + (error.response?.data?.detail || 'Unknown error'));
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
