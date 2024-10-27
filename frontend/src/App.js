import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import CreateAccount from './components/CreateAccount';
import ResetPassword from './components/ResetPassword';
import SetNewPassword from './components/SetNewPassword';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/create-account" element={<CreateAccount />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/set-new-password" element={<SetNewPassword />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
