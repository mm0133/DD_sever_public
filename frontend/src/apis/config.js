import axios from 'axios'


export const get_header = async () => {
    let header = await {};
    const token = await localStorage.getItem('token');
    if (token) {
        header = await {Authorization: `Bearer ${token}`}
    }
    return header
}

export const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    timeout: 5000,
})