import React from 'react';
import { Link } from 'react-router-dom';
import chefHat from '../chefhat.png';

function Header() {
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <header>
      <nav>
        <div className="logo-container">
          <Link to="/">
            <img src={chefHat} alt="Chef Hat" />
          </Link>
        </div>
        <ul className="nav-links">
          {!token ? (
            <>
              <li><Link to="/login" className="button">Login</Link></li>
              <li><Link to="/create-account" className="button">Create Account</Link></li>
              <li><Link to="/reset-password" className="button">Reset Password</Link></li>
            </>
          ) : (
            <>
              <li><Link to="/profile" className="button">Profile</Link></li>
              <li><Link to="/add-recipe" className="button">Add Recipe</Link></li>
              <li><Link to="/reset-password" className="button">Reset Password</Link></li>
              <li><Link to="/" onClick={handleLogout} className="button">Logout</Link></li>
            </>
          )}
        </ul>
      </nav>
    </header>
  );
}

export default Header;
