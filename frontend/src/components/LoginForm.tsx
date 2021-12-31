import React, { useState } from "react";
import authService from "../services/auth.service";


const Login: React.FC = (): JSX.Element => {

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handleLogin = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>): void => {
        console.log('ssssss');
        authService.login(email, password)
        .then(
            (response) => {
                console.log(response)
            },
            (error) => {
                console.log(error.data)
            }
        );
    }

    return (
        <div className="form-container sign-in-container">
            <form action="#">
                <h1>Sign in</h1>
                <input 
                    type="email"
                    placeholder="Email" 
                    onChange={(e) => {setEmail(e.target.value)}}
                />
                <input
                    type="password"
                    placeholder="Password"
                    onChange={(e) => {setPassword(e.target.value)}}
                />
                <a href="#">Forgot your password?</a>
                <button onClick={handleLogin}>Sign In</button>
            </form>
        </div>
    )
}

export default Login;
