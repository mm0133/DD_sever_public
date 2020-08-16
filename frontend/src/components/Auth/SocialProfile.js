import React from "react";
import axios from "axios";

const SocialProfile = () => {
    return (
        <div>
            <div>닉네임</div>
            <input type="text"/>
            <div>이메일</div>
            <input type="text"/>
            <div>핸드폰</div>
            <input type="text"/>
            <button onClick = {() => axios.post({}) }>제출</button>
        </div>
    )
}

export default SocialProfile;