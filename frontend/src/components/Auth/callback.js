import React from "react";
import qs from "qs";
import {api, get_header} from '../../apis/config'
import axios from "axios";


const Callback = ({location}) => {
    const query = qs.parse(location.search, {
        ignoreQueryPrefix: true
    });
    const code = query.code

    const provider = localStorage.getItem('DD_provider')


    const getToken = async () => {
        try{
            const result = await api.post(
                `api/login/social/jwt-pair-user/${provider}`, {
                    provider: provider,
                    code: code
                })
        localStorage.setItem('DD_access', result.data.token);
        localStorage.setItem('DD_refresh', result.data.refresh);
        window.location.href = 'http://127.0.0.1:3000/'
            }catch (err) {
            alert('로그인 실패')
            throw err
            window.location.href = 'http://127.0.0.1:3000/auth/'
        }

    }
    getToken()





    return (
        <div>
        </div>
    );
};


export default Callback;




