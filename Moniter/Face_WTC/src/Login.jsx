// Login.js
import React, { useContext, useState } from 'react';
import { useNavigate, useNavigation } from 'react-router-dom';
import LoginContext from './LoginContext';

function Login() {

  const {SetLoggedAs} = useContext(LoginContext)
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const navigation = useNavigate()

  const handleLogin = () => {
    if (username === 'admin' || username === 'user') {
      console.log(username)
      SetLoggedAs(username)
      navigation('/face')
    } else {
      setError('Invalid username');
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <input
        type="text"
        placeholder="Enter username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default Login;
