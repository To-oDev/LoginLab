import { FaEnvelope, FaLock, FaUser } from "react-icons/fa";
import "./LoginRegister.css";
import { useState } from "react";

const LoginRegister = () => {

    const [action, setAction] = useState('');

    const registerLink = () => {
        setAction(' active')
    }

    const loginLink = () => {
        setAction('')
    }

    const handleLoginRequest = (e) => {
        e.preventDefault();
        console.log('Login', e);
        fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "username": e.target.elements.user.value,
                "password": e.target.elements.password.value,
                "remember_me": e.target.elements.rememberme.value
            })
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            if (data.access_token) {
                localStorage.setItem("token", data.access_token);
                window.location.href = "/"; // Redirigir a la página deseada
            }
        });
    }

    return (
        <div className={`wrapper${action}`}>
            <div className="form-box login">
                <form action="" onSubmit={handleLoginRequest}>
                    <h1>Login</h1>
                    <div className="input-box">
                        <input name="user" type="text" placeholder="Username" required/>
                        <FaUser className="icon"/>
                    </div>
                    <div className="input-box">
                        <input name="password" type="password" placeholder="Password" required/>
                        <FaLock className="icon"/>
                    </div>

                    <div className="remember-forgot">
                        <label><input name="rememberme" type="checkbox"/>Remember me</label>
                        <a href="#">Forgot Password</a>
                    </div>

                    <button type="submit">Login</button>

                    <div className="register-link">
                        <p>Don't have an account? <a href="#" onClick={registerLink}>Register</a></p>
                    </div>
                </form>
            </div>

            <div className="form-box register">
                <form action="">
                    <h1>Registration</h1>
                    <div className="input-box">
                        <input type="text" placeholder="Username" required/>
                        <FaUser className="icon"/>
                    </div>
                    <div className="input-box">
                        <input type="email" placeholder="Email" required/>
                        <FaEnvelope className="icon"/>
                    </div>
                    <div className="input-box">
                        <input type="password" placeholder="Password" required/>
                        <FaLock className="icon"/>
                    </div>

                    <div className="remember-forgot">
                        <label><input type="checkbox"/>I agree to the terms & conditions</label>
                    </div>

                    <button type="submit">Register</button>

                    <div className="register-link">
                        <p>Already have an account <a href=" #" onClick={loginLink}>Login</a></p>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LoginRegister;