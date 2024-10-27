import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/create',
        new URLSearchParams({ name: username, email: email }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      if (response.data.msg) {
        setMessage(response.data.msg);
      } else {
        setMessage('Sign-up successful! Please check your email for verification.');
        setTimeout(() => navigate('/login'), 2000);
      }
    } catch (error) {
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="signupUsername">Username:</label>
        <input
          type="text"
          id="signupUsername"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label htmlFor="signupEmail">Email:</label>
        <input
          type="email"
          id="signupEmail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <button type="submit">Sign Up</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default SignUp;
