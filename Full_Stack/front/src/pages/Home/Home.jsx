import React, { useState } from 'react';
import styles from './Home.module.css';
import { Link, useNavigate } from 'react-router-dom';
function Home() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [password, setPassword] = useState('');
  const [isPasswordCorrect, setIsPasswordCorrect] = useState(false);
  const [dialogMessage, setDialogMessage] = useState('');
  const [showDialog, setShowDialog] = useState(false);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const verifyEmail = () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailRegex.test(email)) {
      setIsEmailValid(true);
    } else {
      setDialogMessage('Please enter a valid email');
      setShowDialog(true);
    }
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const verifyPassword = () => {
    const correctPassword = 'password123';
    if (password === correctPassword) {
      setIsPasswordCorrect(true);
      setDialogMessage('Logged in successfully');
      setShowDialog(true);
      setTimeout(()=>{
        navigate("/resume")
      },500)
    } else {
      setDialogMessage('Incorrect password');
      setShowDialog(true);
    }
  };

  const closeDialog = () => {
    setShowDialog(false);
  };

  return (
    <div className={styles.app}>
      <h1 className={styles.heading}>Interview</h1>
      <div className={styles.form}>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={handleEmailChange}
          className={styles.input_field}
        />
        <button onClick={verifyEmail} className={styles.button}>
          Verify Email
        </button>

        {isEmailValid && (
          <>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={handlePasswordChange}
              className={styles.input_field}
            />
            <button onClick={verifyPassword} className={styles.button}>
              Submit
            </button>
          </>
        )}
      </div>

      {/* Custom dialog box */}
      {showDialog && (
        <div className={styles.dialogOverlay}>
          <div className={styles.dialogBox}>
            <p>{dialogMessage}</p>
            <button onClick={closeDialog} className={styles.dialogButton}>
              OK
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
