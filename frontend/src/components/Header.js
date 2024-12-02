import React from 'react';
import { Link } from 'react-router-dom';
import chefHat from '../chefhat.png';
import axios from "axios";

function Header({onButtonClick}) {
  const token = sessionStorage.getItem('token');
  const auth = sessionStorage.getItem("auth")
  const isAdmin = auth === '2'
  const isUser = auth === '1'

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('auth');
    sessionStorage.removeItem('id');
    sessionStorage.removeItem('name');
    window.location.href = '/';
  };
  const handleCreateRecipe = async () => {
    try {
      const response = await axios.get("https://recipe.naurot.com/recipes/create", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      // console.log("response create_recipe: " + response.data)
      const newTab = window.open()
      newTab.document.open()
      newTab.document.write(response.data)
      newTab.document.close()
    } catch (err) {
      console.error(`ERROR CreateRecipe: ${err}`)
    }
  }

    return (
      <header>
        <nav>
          <div className="logo-container">
            <img src={chefHat} alt="Chef Hat" />
          </div>
          <ul className="nav-links">
            {!token && <li><Link to="/login" className="button">Login</Link></li>}
            {!token && <li><Link to="/create-account" className="button">Create Account</Link></li>}
            {isUser && <li><button onClick={handleCreateRecipe} className="button">Create Recipe</button></li>}
            {isAdmin && <li><button onClick={() => onButtonClick("ing")} className="button">Ingredients</button></li>}
            {isAdmin && <li><button onClick={() => onButtonClick("recipes")} className="button">Recipes</button></li>}
            {isAdmin && <li><button onClick={() => onButtonClick("users")} className="button">Users</button></li>}
            <li><Link to="/reset-password" className="button">Reset Password</Link></li>
            {token && <li><button onClick={handleLogout} className="button">Logout</button></li>}
          </ul>
        </nav>
      </header>
    );
  }

export default Header;
