import {api, get_header} from './config'
import axios from 'axios'



export const social_login_start = async () => {};

export const social_profile_submit = async (email, nickname, phoneNumber) => {
    try {
        const response = await api.post(
            'api/v1/users/my_profile/',
            {email, nickname, phoneNumber}
        );
        console.log(response);
        return response.data
    } catch (err) {
        console.log(err);
        throw err
    }
};

export const social_profile_submit_custom = async (nickname, email, phoneNumber, token) => {
    try {
        const response = await api.post(
            'api/v1/users/my_profile/',
            {email, nickname, phoneNumber},
            {headers: {Authorization: `Bearer ${token}`}}
        );
        console.log(token)
        console.log(response);
        return response.data
    } catch (err) {
        console.log(err);
        throw err
    }
};