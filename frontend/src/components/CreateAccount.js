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
    try {
      const formData = new URLSearchParams();
      formData.append('name', username);
      formData.append('email', email);

      const response = await axios.post('http://localhost:8000/create',
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );

      console.log('Response:', response.data);

      if (response.data.msg) {
        setMessage(response.data.msg);
      } else if (response.data.status === 200) {
        setMessage('Check your email to complete registration');
        setTimeout(() => navigate('/'), 3000);
      }
    } catch (error) {
      console.error('Error details:', error.response || error);
      setMessage('An error occurred: ' + (error.response?.data?.detail || error.message));
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
