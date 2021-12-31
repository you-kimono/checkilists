import axios from "axios";

const API_URL = 'http://localhost:8000/';

class AuthService {

    async login(email: string, password: string) {
        var body = new FormData();
        body.append('username', email);
        body.append('password', password);
        
        axios({
            method: 'post',
            url: API_URL + 'login',
            data: body,
            headers: { "Content-Type": "application/json" },
        })
        .then(response => {
            if (response.data.accessToken) {
                localStorage.setItem('user', JSON.stringify(response.data))
            }
            return response.data
        })
        .catch(error => {
            console.log(error.response.data.detail);
        });
        //return axios.post(API_URL + 'login', {
        //    data: body,
        //})
        //.then(response => {
        //    if (response.data.accessToken) {
        //        localStorage.setItem('user', JSON.stringify(response.data))
        //    }
        //    return response.data
        //});
    }

    async logout() {
        localStorage.removeItem('user');
    }

    async register(email: string, password: string) {
        return axios.post(API_URL + 'register', {
            email,
            password,
        });
    }

    async getCurrentUser() {
        const userStr = localStorage.getItem('user')
        if (userStr) return JSON.parse(userStr);
        return null;
    }

}

export default new AuthService();
