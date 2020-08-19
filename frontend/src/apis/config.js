import axios from 'axios'


export const get_header = async () => {
    let header = {};
    const token = await localStorage.getItem('ddToken');
    if (token) {
        header = {Authorization: `Bearer ${token}`}
    }
    return header
}

export const getTokenAndExpire = async () => {
    const token =  await localStorage.getItem('ddToken') || null;
    const expireDateTime = await localStorage.getItem('ddExpireDateTime') || null;
    return {token, expireDateTime}
}

export const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    timeout: 5000,
})