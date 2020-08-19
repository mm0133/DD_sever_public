import React from "react";
import logo from "../image/logo.png";
import "./Auth.scss";
import {Route} from "react-router-dom";
import {Login, Signup, SocialProfile,} from "../components/Auth";
import Callback from "../components/Auth/callback";
import privateCheck from "../components/Auth/privateCheck";
import PrivateRoute from "../components/utils/PrivateRoute";
import privateCheckSuccess from "../components/Auth/privateCheckSuccess";


const Auth = () => {
    return (
        <div className="total-wrap auth">
            <div className="image"><img src={logo} alt=""/></div>
            <div className="auth-wrap">
                <div className="title">데이타덕 시작하기</div>

                <div className="content">
                    <Route exact path="/auth/login" component={Login}/>
                    <Route path="/auth/signup" component={Signup}/>
                    <Route path="/auth/social_profile" component={SocialProfile}/>
                    <Route path="/auth/social/callback/" component={Callback}/>
                    <PrivateRoute path="/auth/private" component={privateCheckSuccess}/>
                </div>
            </div>
        </div>
    )
}

export default Auth;