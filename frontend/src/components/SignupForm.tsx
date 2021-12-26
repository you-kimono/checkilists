import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
const axios = require('axios');


interface IProps {
    onClick: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}

const Signup: React.FC<IProps> = ({ onClick }): JSX.Element => {

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [repeat_password, setRepeatPassword] = useState('')

    //const handleClick = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    const handleClick = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>): void => {
        onClick(e)
        if (
            !email
            || !password
            || !repeat_password
            || password != repeat_password
        ) {
            return;
        } else {
            console.log('facciamo partire la richiesta');
            axios.post('http://localhost:8000/register', {
                username: email,
                password: password
            })
            .then(function(response) {
                if (response.data.token) {
                    console.log('token: ' + response.data.token)
                }
            })
            .catch(function (error) {
                console.log('error: ' + error)
            })
        }
    }

    return (
        <div className="form-container sign-up-container">
            <form action="#">
                <h1>Create Account</h1>
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
                <input
                    type="password"
                    placeholder="Repeat password"
                    onChange={(e) => {setRepeatPassword(e.target.value)}}
                />
                <button onClick={handleClick}>Sign Up</button>
            </form>
        </div>
    )
}

export default Signup;
