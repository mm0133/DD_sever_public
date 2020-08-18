import React from "react";
import axios from "axios";
import {socialLoginStart, socialProfileSubmit} from "../../apis/api";

const SocialProfile = () => {
    return (
        <div>
            <div>닉네임</div>
            <input id="nickname" type="text"/>
            <div>이메일</div>
            <input id="email" type="text"/>
            <div>핸드폰</div>
            <input id="phoneNumber" type="text"/>
            <button onClick = {
                () => socialProfileSubmit(
                document.querySelector('#nickname').value,
                document.querySelector('#email').value,
                document.querySelector('#phoneNumber').value
            ) }>제출</button>
        </div>
    )
}

export default SocialProfile;