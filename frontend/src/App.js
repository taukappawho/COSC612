import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import CreateAccount from './components/CreateAccount';
import ResetPassword from './components/ResetPassword';
import SetNewPassword from './components/SetNewPassword';
import AddRecipe from './components/AddRecipe';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/create-account" element={<CreateAccount />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/verify" element={<SetNewPassword />} />
          <Route path="/add-recipe" element={<AddRecipe />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
