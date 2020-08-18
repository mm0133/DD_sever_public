import React from "react";
import {NavLink} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faGithub, faGoogle} from "@fortawesome/free-brands-svg-icons";
import "./Login.scss";

const googleaddress='https://accounts.google.com/o/oauth2/auth?client_id=468545293049-p195m8hbli0ss99614cb2siqf4rgt04k.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:3000/auth/social/callback/&response_type=code&scope=email'

const Login = () => {
    return (
        <div className="total-wrap">
            <div className="signup">
                <div>계정이 없으신가요?</div>
                <NavLink to="/auth/signup" className="link">
                    <div className="button">
                        <div className="overlay">회원가입 바로가기 <span>></span></div>
                    </div>
                </NavLink>
            </div>

            <div className="login">
                <div className="input">
                    <div className="name">아이디</div>
                    <input type="text"/>
                </div>
                <div className="input">
                    <div className="name">비밀번호</div>
                    <input type="password"/>
                </div>
                <button>로그인</button>
            </div>

            <div className="division">
                <div className="line"></div>
                <div className="or">OR</div>
                <div className="line"></div>
            </div>

            <div className="social-wrap">
                <button className="social google" onClick={() => {localStorage.setItem('DD_provider', 'google-oauth2')
        window.location.href = googleaddress;}}>
                    <FontAwesomeIcon icon={faGoogle} className="icon"/>
                    <div className="text">Google로 시작하기</div>
                </button>
                <button className="social naver">
                    <div className="icon">N</div>
                    <div className="text">네이버로 시작하기</div>
                </button>
                <button className="social github">
                    <FontAwesomeIcon icon={faGithub} className="icon"/>
                    <div className="text">GitHub로 시작하기</div>
                </button>
            </div>
        </div>
    )
}

export default Login;
