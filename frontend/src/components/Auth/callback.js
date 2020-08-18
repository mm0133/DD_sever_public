import React, {useEffect, useState} from "react";
import qs from "qs";
import {api, get_header} from '../../apis/config'
import {socialProfileSubmitCustom} from "../../apis/api";


const Callback = ({location}) => {
    const [token, setToken] = useState("");
    const [showRender, setShowRender] = useState(false);

    useEffect(() => {
        console.log('hello');

        async function wow() {
            console.log('wow');
            const query = qs.parse(location.search, {
                ignoreQueryPrefix: true
            });
            const code = query.code;

            const provider = localStorage.getItem('DD_provider')

            const getToken = async () => {
                const result = await api.post(
                    `api/login/social/jwt-pair-user/${provider}`, {
                        provider: provider,
                        code: code
                    });
                const url = 'api/v1/users/has_profile/';
                console.log(result.data.token);
                await setToken(result.data.token);
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

                    localStorage.setItem('DD_access', result.data.token);
                    localStorage.setItem('DD_refresh', result.data.refresh);
                    window.location.href = 'http://127.0.0.1:3000/'
                }
                else {
                    setShowRender(true)
                }
            };
            await getToken();
        }
        wow();
    }, []);

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
                        () => socialProfileSubmitCustom(
                            document.querySelector('#nickname').value,
                            document.querySelector('#email').value,
                            document.querySelector('#phoneNumber').value,
                            token
                        )}>제출
                    </button>
                </div>
            }
        </div>
    );
};


export default Callback;




