import React from "react";
import logo from "../image/logo.png";
import "./Auth.scss";
import {Route} from "react-router-dom";
import {Login, Signup} from "../components/Auth";

const Auth = () => {
    return (
        <div className="total-wrap auth">
            <div className="image"><img src="" alt=""/></div>
            <div className="auth-wrap">
                <div className="title">데이타덕 시작하기</div>

                <div className="content">
                    <Route exact path="/auth" component={Login}/>
                    <Route path="/auth/signup" component={Signup}/>
                </div>
            </div>
        </div>
    )
}

export default Auth;