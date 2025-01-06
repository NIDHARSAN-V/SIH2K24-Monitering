import React from "react";
import toast from "react-hot-toast";
import axios from "axios";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ProfileImage from './user_149071.png';
import style from './Login.module.css';
import ClipLoader from 'react-spinners/ClipLoader';

function Login() {
  localStorage.clear();
  const [loading, setloading] = useState(false);
  const [email, setemail] = useState('');
  const [password, setpassword] = useState('');
  const navigate = useNavigate();

  const onFinish = async () => {
    const user = {
      email,
      password,
    };

    try {
      setloading(true);
      const response = await axios.post("http://localhost:5500/api/user/login", user);

      setloading(false);

      const { token, user: userData } = response.data;
      if (userData) {
        localStorage.setItem("token", token);
        toast.success("Login Successful!");
        if (userData.isAdmin) {
          navigate('/admin');
        }
        else if (userData) {
          navigate('/');
        }
      } else {
        toast.error(response.data);
      }
    } catch (error) {
      console.log(error);
      setloading(false);
      toast.error("Login failed!");
    }
  };

  return (
    <div className={style.LoginMain}>
      {loading && (
        <div className={style.loader_overlay}>
          <ClipLoader color="#2AA7FF" size={50} />
        </div>
      )}

      <div className={style.LoginBox}>
        <div className={style.LoginHeader}>
          <div className={style.Loginimage}><img src={ProfileImage} alt="Profile" /></div>
          <div className={style.LoginHead}>Login</div>
        </div>
        <div className={style.LoginContent}>
          <div className={style.email}>
            <i className="ri-mail-line"></i>
            <input type="text" placeholder="email" value={email} onChange={(e) => { setemail(e.target.value) }} />
          </div>
          <div className={style.password}>
            <i className="ri-lock-line"></i>
            <input type="password" placeholder="Password" value={password} onChange={(e) => { setpassword(e.target.value) }} />
          </div>
          <button onClick={onFinish} className={style.LoginButton}>Login</button>
          <Link to="/register" className="anchor mt-2">
            CLICK HERE TO REGISTER
          </Link>
        </div>
      </div>
    </div>

  );
}

export default Login;
