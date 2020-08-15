import React, {useEffect, useState} from "react";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCalendar, faStar, faTrophy, faUser} from "@fortawesome/free-solid-svg-icons";

import {getContestDetail} from "../Api";
import {NavLink, Route} from "react-router-dom";
import ContestOverview from "../components/ContestOverview";
import ContestData from "../components/ContestData";

import {getDDay, getDifficulty, getIsFinished, getIsForTraining} from "../Utils";

import "./ContestDetail.scss";
import ContestCommunity from "../components/ContestCommunity";
import ContestCodenote from "../components/ContestCodenote";
import ContestRanking from "../components/ContestRanking";


const ContestDetail = ({match}) => {
    const [contest, setContest] = useState([]);

    useEffect(() => {
        const init = async () => {
            const data = await getContestDetail(match.params.id);
            console.log(data);

            setContest(data);
        }
        init();
    }, [])

    console.log(contest);

    const prize = contest.isForTraining ? "연습" : `${contest.prize}만`;
    const dDay = getDDay(`${contest.deadline}`);
    console.log(contest.difficulty);


    const difficulty = contest.difficulty ? getDifficulty(contest.difficulty).type : null;
    const colorDifficulty = contest.difficulty ? getDifficulty(contest.difficulty).color : null;

    const training = getIsForTraining(contest.isForTraining);
    const finish = getIsFinished(contest.isFinished);

    const activeStyle = {
        fontFamily: "NanumSquareExtraBold",
        color: "#333333",
        padding: "10px 5px 4px 5px",
        borderBottom: "6px solid #4b6580",
        boxSizing: "border-box"
    }

    return (
        <div>
            {!contest ? <div>Error</div> :
                <div className="total-wrap contest-detail">
                    <div className="detail-main-banner" style={{backgroundImage: `url(${contest.backThumb})`}}>
                        <div className="top-side">
                            <div className="text">
                                <div>{training}<span>ㅣ</span>{finish}</div>
                                <div className="difficulty">
                                    <div className="circle" style={{backgroundColor: `${colorDifficulty}`}}/>
                                    {difficulty}
                                </div>
                            </div>
                            <FontAwesomeIcon icon={faStar} className="icon"/>
                        </div>
                        <div>
                            <div className="title">{contest.title}</div>
                            <div className="subtitle">{contest.subtitle}</div>
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
                                    <FontAwesomeIcon icon={faTrophy} className="icon"/>
                                </div>
                                <div>{prize}</div>
                            </div>
                        </div>
                    </div>

                    <div className="detail-nav">
                        <NavLink to={`/contest/${match.params.id}/overview`} className="link" activeStyle={activeStyle}>대회
                            안내</NavLink>
                        <NavLink to={`/contest/${match.params.id}/data`} className="link"
                                 activeStyle={activeStyle}>데이터</NavLink>
                        <NavLink to={`/contest/${match.params.id}/community`} className="link"
                                 activeStyle={activeStyle}>토론방</NavLink>
                        <NavLink to={`/contest/${match.params.id}/codenote`} className="link"
                                 activeStyle={activeStyle}>코드공유</NavLink>
                        <NavLink to={`/contest/${match.params.id}/ranking`} className="link"
                                 activeStyle={activeStyle}>랭킹</NavLink>
                    </div>

                    <contents>
                        <Route
                            path={`/contest/${match.params.id}/overview`}
                            component={() => <ContestOverview
                                deadline={contest.deadline}
                                timeline={contest.timeline}
                                contestExplanation={contest.contestExplanation}
                                evaluationExplanation={contest.evaluationExplanation}
                                prizeExplanation={contest.prizeExplanation}
                            />}
                        />
                        <Route
                            path={`/contest/${match.params.id}/data`}
                            component={() => <ContestData
                                dataExplanation={contest.dataExplanation}
                            />}
                        />
                        <Route
                            path={`/contest/${match.params.id}/community`}
                            component={ContestCommunity}
                        />
                        <Route
                            path={`/contest/${match.params.id}/overview`}
                            component={ContestCodenote}
                        />
                        <Route
                            path={`/contest/${match.params.id}/ranking`}
                            component={ContestRanking}
                        />
                    </contents>
                </div>
            }
        </div>
    )
}

export default ContestDetail;