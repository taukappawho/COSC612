import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const Login = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !password) {
      setError('Username and password are required');
      return;
    }
    try {
      const response = await axios.post('https://recipe.naurot.com/login', {
        name,
        password
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

     // Retrieve the Authorization header
    const token = response.data['token']; // Headers are case-insensitive
    const [header, payload, signature] = token.split(".")
    const decodedPayload = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
    // Store the token and payload values in sessionStorage
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('name', decodedPayload.sub); // Store 'sub' from payload
    sessionStorage.setItem('auth', decodedPayload.auth); // Store 'auth' from payload
    sessionStorage.setItem('id', decodedPayload.id); // Store 'id' from payload

    // Navigate to the homepage
    navigate('/');

   } catch (error) {
     console.error('Error during login:', error.message);
 
     // Handle errors from the server or network
     setError(
       'Login failed: ' +
         (error.response?.data?.message || 'An unexpected error occurred')
     );
   }
 };

 function base64URLDecode(base64Url){
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const paddedBase64 = base64.padEnd(base64.length + (4 - base64.length % 4) % 4, "=");
  return atob(paddedBase64);
 }
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
