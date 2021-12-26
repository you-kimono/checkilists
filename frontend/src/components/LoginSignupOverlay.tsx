import { useEffect } from 'react'


function LoginSignupOverlay() {

    useEffect(() => {
        const signUpButton = document.getElementById('signUp');
        const signInButton = document.getElementById('signIn');
        const container = document.getElementById('container');
        signUpButton && signUpButton.addEventListener('click', () => {
            container && container.classList.add("right-panel-active");
        });
        signInButton && signInButton.addEventListener('click', () => {
            container && container.classList.remove("right-panel-active");
        });
    })

    return (
        <div className="overlay-container">
            <div className="overlay">
                <div className="overlay-panel overlay-left">
                    <h1>Welcome Back!</h1>
                    <p>To keep connected with us please login with your personal info</p>
                    <button className="ghost" id="signIn">Sign In</button>
                </div>
                <div className="overlay-panel overlay-right">
                    <h1>Hello, Friend!</h1>
                    <p>Enter your personal details and start journey with us</p>
                    <button className="ghost" id="signUp">Sign Up</button>
                </div>
            </div>
        </div>
    )
}

export default LoginSignupOverlay;
