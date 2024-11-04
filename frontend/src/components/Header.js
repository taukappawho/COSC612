import React from 'react';
import { Link } from 'react-router-dom';
import chefHat from '../chefhat.png';

function Header() {
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <header>
      <nav>
        <div className="logo-container">
          <img src={chefHat} alt="Chef Hat" />
        </div>
        <ul className="nav-links">
          {!token && <li><Link to="/login" className="button">Login</Link></li>}
          {!token && <li><Link to="/create-account" className="button">Create Account</Link></li>}
          <li><Link to="/reset-password" className="button">Reset Password</Link></li>
          {token && <li><button onClick={handleLogout} className="button">Logout</button></li>}
        </ul>
      </nav>
    </header>
  );
}

export default Header;
