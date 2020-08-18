import {api, get_header} from './config'
import axios from 'axios'

const SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '468545293049-p195m8hbli0ss99614cb2siqf4rgt04k.apps.googleusercontent.com'
const CLIENT_SECURITY_SECRET = 'AAuWqQMocFaaeXmbR0rA3wiZ'
export const social_login_start = async () => {
    try {
        // const result = axios.get(
        //     'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.labels&access_type=offline&include_granted_scopes=true&state=state_parameter_passthrough_value&redirect_uri=http%3A%2F%2F127.0.0.1%3A3000&response_type=code&client_id=186484694334-b9ln0thobq7vm6t13hb0ef9gnpf9r39f.apps.googleusercontent.com&flowName=GeneralOAuthFlow'
        // )
        // console.log(result)
        console.log("post did it")
        const response = await api.post(
            `api/login/social/jwt-pair/`,
            {
                provider: "google-oauth2",
                code: SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                // redirectUri: window.location.origin + '/'
            }
        )
        return response.data
    } catch (err) {
        console.log(err)
        throw err
    }
}

export const test = async (nickname) => {
    const header = get_header();
    const url = ''
    const result = api.post(
        url,
        {nickname },
        {headers:header}
    )
}

export const test2 = async (nickname) => {
    const headers = get_header();
    const url = ''

    const result = api.get(
        url,
        {headers}
    )
}

export const social_profile_submit = async (email, nickname, phoneNumber) => {
    try {
        const response = await api.post(
            'login/social/profile/',
            {email, nickname, phoneNumber}
        )
        console.log(response)
        return response.data
    } catch (err) {
        console.log(err)
        throw err
    }
}