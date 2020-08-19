import React, {useEffect, useState} from "react";
import qs from "qs";
import {api, get_header} from '../../apis/config'
import {socialProfileSubmit, socialProfileSubmitCustom} from "../../apis/api";


const Callback = ({location}) => {

    const [token, setToken] = useState('');
    const [refresh, setRefresh] = useState('');
    const [showRender, setShowRender] = useState(false);

    useEffect(() => {
        console.log('hello');
        async function wow() {
            console.log('wow');
            const query = qs.parse(location.search, {
                ignoreQueryPrefix: true
            });
            const code = query.code;

            const provider = sessionStorage.getItem('DD_provider')

            const getToken = async () => {
                const result = await api.post(
                    `api/login/social/jwt-pair-user/${provider}`, {
                        provider: provider,
                        code: code,
                        state: 'dataduck'
                    });
                const url = 'api/v1/users/has_profile/';
                console.log(result.data.token);
                await setToken(result.data.token);
                await setRefresh(result.data.refresh)
                const token2 = result.data.token;
                const header = {Authorization: `Bearer ${token2}`};


                const result2 = await api.post(
                    url,
                    {},
                    {headers: header}
                );
                console.log(result2);
                console.log(result2.data);
                const hasProfile = (result2.data === 'true');


                console.log(hasProfile)
                if (hasProfile === true) {

                    localStorage.setItem('ddToken', result.data.token);
                    localStorage.setItem('ddRefreshToken', result.data.refresh);
                    const date = new Date()
                    localStorage.setItem('ddExpireDateTime', date.getTime());
                    window.location.href = 'http://127.0.0.1:3000/'
                } else {
                    setShowRender(true)
                }
            };
            await getToken();
        }

        wow();
    }, []);

    const setItems = async (token, refresh) => {
        let dt = await new Date()
        console.log(dt)
        dt.setHours(dt.getHours() + 6);
        localStorage.setItem('ddToken', token);
        localStorage.setItem('ddRefreshToken', refresh);
        localStorage.setItem('ddExpireDateTime', dt.getTime());
    }

    return (
        <div>
            {!showRender ?
                <div>loading</div> :
                <div>
                    <div>닉네임</div>
                    < input id="nickname" type="text"/>
                    <div>이메일</div>
                    <input id="email" type="text"/>
                    <div>핸드폰</div>
                    <input id="phoneNumber" type="text"/>
                    <button onClick={

                        async () => {
                            await socialProfileSubmitCustom(
                                document.querySelector('#nickname').value,
                                document.querySelector('#email').value,
                                document.querySelector('#phoneNumber').value,
                                token)
                            await setItems(token, refresh);
                            window.location.href = 'http://127.0.0.1:3000/'
                        }}>제출
                    </button>
                </div>
            }
        </div>
    );
};


export default Callback;




