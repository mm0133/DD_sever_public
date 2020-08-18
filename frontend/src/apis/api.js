import {api, get_header} from './config'
import axios from 'axios'



export const social_login_start = async () => {}

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