import React from "react";
import "./header.scss"


function Header() {
    return (
        <div id="total-wrap">
            <header>
                <div className="logo">데이타덕 <span>Data</span>Duck</div>
                <div className="nav">
                    <div className="nav-item">대회 목록</div>
                    <div className="nav-item">강의</div>
                    <div className="nav-item">토론방</div>
                    <div className="nav-item">코드 공유</div>
                    <div className="nav-item">사용설명서</div>
                    <div className="nav-item">공지</div>
                    <div className="nav-item">마이페이지</div>
                </div>
                <div className="logout">로그아웃</div>
            </header>
        </div>
    )
}

export default Header;