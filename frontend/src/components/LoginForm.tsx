import React from "react";


const Login: React.FC = (): JSX.Element => {

    return (
        <div className="form-container sign-in-container">
            <form action="#">
                <h1>Sign in</h1>
                <input type="email" placeholder="Email" />
                <input type="password" placeholder="Password" />
                <a href="#">Forgot your password?</a>
                <button>Sign In</button>
            </form>
        </div>
    )
}

export default Login;
