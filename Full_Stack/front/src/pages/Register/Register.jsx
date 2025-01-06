// UserRegister.js
import React, { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";
import styles from "./Register.module.css";

function Register() {
    const [loading, setLoading] = useState(false);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');


    const navigate = useNavigate();

    const onFinish = async () => {
        const userData = {
            name,
            email,
            password,

        };
        try {
            setLoading(true);
            const response = await axios.post("http://localhost:5500/api/user/register", userData);
            setLoading(false);
            if (response.data.success) {
                toast.success(response.data.message);
                navigate("/login");
            } else {
                toast.error(response.data.message);
            }
        } catch (error) {
            toast.error("Something went wrong");
        }
    };

    return (
        <div className={styles.registerMain}>
            <div className={styles.container}>
                {loading && (<h1>Loading</h1>)}

                <h2>Register</h2>
                <input type="text" className={styles["form-control"]} placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
                <input type="text" className={styles["form-control"]} placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <input type="password" className={styles["form-control"]} placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />

                <button className={styles["btn-primary"]} onClick={onFinish}>Register</button>
                <Link to="/login" className={styles.anchor}>
                    Already Have an Account
                </Link>
            </div>
        </div>
    );
}

export default Register;
