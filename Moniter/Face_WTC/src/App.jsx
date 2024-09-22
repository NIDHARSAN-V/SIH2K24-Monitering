import React from 'react';
import { BrowserRouter as Router, Route, Routes, BrowserRouter } from 'react-router-dom';
import Face from './Face';
import Login from './Login';
import { LoginProvider } from './LoginContext';

function App() {
  return (
    <LoginProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/face" element={<Face />} />
        </Routes>
      </BrowserRouter>
    </LoginProvider>
  );
}

export default App;
