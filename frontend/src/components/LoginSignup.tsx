import React from 'react';
import Signup from './SignupForm';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import LoginSignupOverlay from './LoginSignupOverlay';

const LoginSignup: React.FC = (): JSX.Element => {

    const register = () => {
        console.log('clicked!')
    }
    return (
        <div className="container" id="container">
            <SignupForm onClick={register} />
            <LoginForm />
            <LoginSignupOverlay />
        </div>

    );
}

export default LoginSignup;
