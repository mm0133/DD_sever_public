import React from "react";
import "./Header.scss"
import {NavLink} from "react-router-dom";


function Header() {
    const activeStyle = {
        fontFamily: "NanumSquareBold",
        opacity: 1
    }
    return (
        <div className="total-wrap">
            <header>
                <NavLink to="/" className="link">
                    <div className="logo">데이타덕 <span>Data</span>Duck</div>
                </NavLink>
                <div className="nav">
                    <NavLink to="/contest" className="link nav-item" activeStyle={activeStyle}>대회 목록</NavLink>
                    <NavLink to="/education" className="link nav-item" activeStyle={activeStyle}>강의</NavLink>
                    <NavLink to="/debate" className="link nav-item" activeStyle={activeStyle}>토론방</NavLink>
                    <NavLink to="/codenote" className="link nav-item" activeStyle={activeStyle}>코드 공유</NavLink>
                    <NavLink to="/manual" className="link nav-item" activeStyle={activeStyle}>사용설명서</NavLink>
                    <NavLink to="/notice" className="link nav-item" activeStyle={activeStyle}>공지</NavLink>
                    <NavLink to="/mypage" className="link nav-item" activeStyle={activeStyle}>마이페이지</NavLink>
                </div>
                <div className="logout">로그아웃</div>
            </header>
        </div>

    )
}

export default Header;