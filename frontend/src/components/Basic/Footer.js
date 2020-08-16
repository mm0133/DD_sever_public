import React from "react";
import "./Footer.scss";

const Footer = () => {
    return (
        <div className="total-wrap">
            <footer>
                <div className="left-side">
                    <div className="title">데이타덕 <span>Data</span>Duck</div>
                    <div className="copyright">Copyright © Daor. All right reversed.</div>
                </div>
                <div className="right-side">
                    <div>이용약관</div>
                    <div className="bar">ㅣ</div>
                    <div>개인정보처리방침</div>
                </div>
            </footer>
        </div>
    )
}

export default Footer;