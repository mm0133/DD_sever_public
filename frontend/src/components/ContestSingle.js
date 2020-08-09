import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCalendar, faTrophy, faUser} from "@fortawesome/free-solid-svg-icons";
import {faStar as faStarLine} from "@fortawesome/free-regular-svg-icons";

import {getDDay, getDifficulty, getEvaluation} from "./Utils" // D-day 계산 함수

import "./ContestSingle.scss";


const ContestSingle = (props) => {
    const prize = props.isForTraining ? "연습" : `${props.prize}만`;
    const dDay = getDDay(`${props.deadline}`);
    const difficulty = getDifficulty(props.difficulty).type;
    const colorDifficulty = getDifficulty(props.difficulty).color;
    const evaluation = getEvaluation(props.evaluationMethod);

    return (
        <div className="contest">
            <div className="content-wrap">
                <div className="contest-image"><img src={props.profileThumb} alt=""/></div>
                <div className="content">
                    <div>
                        <div className="title">{props.title}<span>{prize}</span></div>
                        <div className="subtitle">
                            {props.subtitle}
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
                            <div>D-{dDay}</div>
                        </div>
                        <div className="summary">
                            <div className="icon-wrap">
                                <FontAwesomeIcon icon={faTrophy} className="icon trophy"/>
                            </div>
                            <div>{evaluation}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="participate">
                <div className="top-side">
                    <div className="difficulty">
                        <div className="circle" style={{backgroundColor: `${colorDifficulty}`}} />
                        {difficulty}
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