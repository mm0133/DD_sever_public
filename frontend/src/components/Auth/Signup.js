import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faUser} from "@fortawesome/free-solid-svg-icons";
import "./Signup.scss";

const Signup = () => {
    return (
        <div className="total-wrap">
            <div className="signup-title">
                <div className="icon-wrap">
                    <FontAwesomeIcon icon={faUser} className="icon"/>
                </div>
                <div>회원가입</div>
            </div>

            <div className="input-wrap">
                <div className="top-side">
                    <div className="input">
                        <div className="text">아이디</div>
                        <input type="text"/>
                    </div>
                    <div className="input">
                        <div className="text">비밀번호</div>
                        <input type="text"/>
                    </div>
                    <div className="input">
                        <div className="text">비밀번호 확인</div>
                        <input type="text"/>
                    </div>
                </div>

                <div className="bottom-side">
                    <div className="input">
                        <div className="text">이메일</div>
                        <input type="text"/>
                    </div>
                    <div className="input with-notice">
                        <div className="text">전화번호</div>
                        <div>
                            <input type="text"/>
                            <div className="notice">
                                상금 수령을 위해 정확히 입력해주세요.
                            </div>
                        </div>
                    </div>
                    <div className="input with-notice">
                        <div className="text">닉네임</div>
                        <div>
                            <input type="text"/>
                            <div className="notice">
                                데이타덕에서 사용하는 이름입니다.
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="button">
                <button>
                    <div className="overlay">회원가입</div>
                </button>
            </div>
        </div>
    )
}

export default Signup;