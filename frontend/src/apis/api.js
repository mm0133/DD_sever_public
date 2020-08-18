import {api, get_header} from './config'
import axios from 'axios'


export const socialLoginStart = async () => {
};

export const socialProfileSubmit = async (email, nickname, phoneNumber) => {
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
}

export const socialProfileSubmitCustom = async (nickname, email, phoneNumber, token) => {
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
}

export const getContestList = async () => {
    try {
        const response = await axios.get(
            "api/v1/contests/contest/",
            {headers: {Authorization: `Bearer ${token}`}}
        );
        return response.data;
    } catch (err) {
        console.log(err);
        throw err
    }
}

export const getContestDetail = async (num) => {
    try {
        const response = await axios.get(
            `api/v1/contests/contest/${num}/`,
            {headers: {Authorization: `Bearer ${token}`}}
        );
        return response.data;
    } catch (err) {
        console.log(err);
        throw err
    }
}

export const getContestDebate = async () => {
    try {
        const response = await axios.get(
            "api/v1/communications/contestdebate/",
            {headers: {Authorization: `Bearer ${token}`}}
        );
        return response.data;
    } catch (err) {
        console.log(err);
        throw err
    }
}