import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCalendar, faTrophy, faUser} from "@fortawesome/free-solid-svg-icons";
import {faStar as faStarLine} from "@fortawesome/free-regular-svg-icons";

import "./ContestSingle.scss";

const ContestSingle = (props) => {
    return (
        <div className="contest">
            <div className="content-wrap">
                <div className="contest-image"><img src="" alt=""/></div>
                <div className="content">
                    <div>
                        <div className="title">{props.title}<span>{props.prize}만</span></div>
                        <div className="subtitle">
                            8개의 감정을 기준으로 얼굴 사진 분류하기
                            <span className="bar">ㅣ</span>
                            <span className="classification">{props.learningModel}</span>
                        </div>
                    </div>
                    <div className="summary-wrap">
                        <div className="summary">
                            <div className="icon-wrap">
                                <FontAwesomeIcon icon={faUser} className="icon"/>
                            </div>
                            <div>20팀</div>
                        </div>
                        <div className="summary">
                            <div className="icon-wrap">
                                <FontAwesomeIcon icon={faCalendar} className="icon"/>
                            </div>
                            <div>D-120</div>
                        </div>
                        <div className="summary">
                            <div className="icon-wrap">
                                <FontAwesomeIcon icon={faTrophy} className="icon trophy"/>
                            </div>
                            <div>정확도 Accuracy</div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="participate">
                <div className="top-side">
                    <div className="difficulty">
                        <div className="circle"></div>
                        {props.difficulty}
                    </div>
                    <FontAwesomeIcon icon={faStarLine} className="scrap"/>
                </div>
                <div className="button">
                    <div className="overlay">
                        참가하기
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ContestSingle;